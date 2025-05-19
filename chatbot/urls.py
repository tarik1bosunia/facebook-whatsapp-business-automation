from django.urls import path
from .views import chat_with_gemini

urlpatterns = [
    path('api/chat/', chat_with_gemini, name='chat-with-gemini'),
]
