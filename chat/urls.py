from django.urls import path

from .views import index, room, ping


app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('ping/', ping, name='ping'),
    path('<str:room_name>/', room, name='room'),
]
