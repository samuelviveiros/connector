from django.urls import path
from .views import home, logout_view, register_creator

app_name = 'creators'

urlpatterns = [
    path('', home, name='home'),
    path('accounts/logout/', logout_view, name='logout'),
    path('register_creator/', register_creator, name='register_creator')
]
