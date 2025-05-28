# messenger/urls.py
from django.urls import include, path
from . import views

from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, ChatMessageViewSet, send_message

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', ChatMessageViewSet, basename='chatmessage')
# router.register(r'users', SocialMediaUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-message/', send_message, name='send_message'),
    path('webhook/', views.messaging_webhook, name='messenging_webhook'),
    # path('api/chats/', views.ChatHistoryView.as_view(), name='chat-history'),
    # path('api/messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
]
