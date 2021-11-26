import asyncio
import os

# asgiref 3.4.1 is causing issues. See: https://stackoverflow.com/a/68553668/16196935
from asgiref.sync import sync_to_async

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import telethon as tg

from .models import Creator, Message
from .serializers import CreatorSerializer


api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


# def get_event_loop():
#     if hasattr(get_event_loop, '_loop'):
#         return getattr(get_event_loop, '_loop')

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)

#     setattr(get_event_loop, '_loop', loop)
#     return loop

def get_new_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


# TIP1: To logout the user, access the following URL:
# http://127.0.0.1:8000/accounts/logout/

# TIP2: More info: https://www.youtube.com/watch?v=dBctY3-Z5hY


def home(request):
    if not request.user.is_authenticated:
        #return redirect('accounts/login/')  # using relative path
        return redirect('login')  # using path name

    return render(request, 'creators/home.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')  # using path name


@login_required
def register_creator(request):
    return render(request, 'creators/register_creator.html')


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer

    # This will make this view login required
    permission_classes = (IsAuthenticated,)


class CustomEndpoint(APIView):
    def get(self, request):
        return Response({"ObiWanSaid": "Hello There!"})


#
# Obter o histórico de chat vai ser complicado. Primeiro porque
# a função a seguir é assíncrona. Devido a esse fato, assim que
# uma view chamar essa função, a view já retornará de imediato
# uma resposta para o browser.
#
# O problema em si será retornar a resposta da função assíncrona
# abaixo para o browser. A princípio, há duas abordagens possíveis:
#
# 1) Salvar o resultado no banco de dados. Enquanto isso, o browser
# ficará executando um timer cuja função callback consultará o banco
# para obter o resultado. Essa é a implementação mais fácil, porém
# menos sofisticada, eu diria.
#
# 2) Utilizar WebSockets. Assim que o resultado estiver pronto,
# uma mensagem contendo o resultado será enviada para o browser.
# Essa seria a solução mais sofisticada, porém mais complicada
# de implementar.
# 3) HTTP long polling. Pesquisar sobre isso.
#
async def telegram_chat_history(client, phone):
    messages = []
    me = await client.get_me()

    async for message in client.iter_messages(phone):
        text = '[FILE]' if message.media else message.text
        side = 'right' if message.sender == me else 'left'
        messages.insert(0, {
            'text': text,
            'side': side,
        })

    await telegram_chat_history_to_db(phone, messages)


@sync_to_async
def telegram_chat_history_to_db(phone, messages):
    creator = Creator.objects.get(phone=phone)

    # def print_messages():
    #     print(creator.messages.values('message'))

    with transaction.atomic():
        creator.messages.all().delete()
        creator.messages.bulk_create([
            Message(
                creator=creator,
                text=message['text'],
                side=message['side']
            ) for message in messages
        ])

        # transaction.on_commit(lambda: print_messages())


class ChatHistoryRequest(APIView):
    def get(self, request, phone):
        client = tg.TelegramClient('telegram.session', api_id, api_hash, loop=get_new_event_loop())
        with client:
            client.loop.run_until_complete(telegram_chat_history(client, phone))

        return Response({
            "phone": phone,
            "telethon": tg.__version__,
        })


class ChatHistoryResponse(APIView):
    def get(self, request, phone):
        messages = Creator.objects.get(phone=phone).messages.values('text', 'side')
        return Response(messages)


async def telegram_send_message(client, phone, message):
    await client.send_message(phone, message)


class TelegramSendMessage(APIView):
    def post(self, request, phone, message):
        client = tg.TelegramClient('telegram.session', api_id, api_hash, loop=get_new_event_loop())
        with client:
            client.loop.run_until_complete(
                telegram_send_message(client, phone, message)
            )

        return Response({
            "phone": phone,
            "message": message,
            "telethon": tg.__version__,
        })
