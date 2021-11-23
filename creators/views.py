from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Creator
from .serializers import CreatorSerializer

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
