from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def ping(request):
    import channels.layers
    from asgiref.sync import async_to_sync

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('chat_foo', {
        'type': 'chat_message',
        'message': 'ping'
    })

    return HttpResponse('<h1>PING!</h1>')
