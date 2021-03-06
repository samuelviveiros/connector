from django.urls import path, include
from rest_framework import routers

from .views import (
    home,
    logout_view,
    register_creator,
    CreatorViewSet,
    CustomEndpoint,
    ChatHistoryRequest,
    ChatHistoryResponse,
    TelegramSendMessage,
)

app_name = 'creators'

router = routers.DefaultRouter()
router.register('creators', CreatorViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('accounts/logout/', logout_view, name='logout'),
    path('register_creator/', register_creator, name='register_creator'),
    path('v1/', include(router.urls)),
    path('v1/custom-endpoint/', CustomEndpoint.as_view(), name='custom-endpoint'),
    path('v1/telegram/chat-history-request/<str:phone>/', ChatHistoryRequest.as_view(), name='chat-history-request'),
    path('v1/telegram/chat-history-response/<str:phone>/', ChatHistoryResponse.as_view(), name='chat-history-response'),
    path('v1/telegram/send-message/<str:phone>/<str:message>/', TelegramSendMessage.as_view(), name='send-message'),
]
