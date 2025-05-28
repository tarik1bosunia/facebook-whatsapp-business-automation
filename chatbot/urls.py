from django.urls import path
from .views import chat_with_ai

urlpatterns = [
    path('api/chat/', chat_with_ai, name='chat-with-ai'),
]
