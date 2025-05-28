from django.urls import path
from .views import WhatsAppMessageAPI, whatsapp_webhook

urlpatterns = [
    path('webhook/', whatsapp_webhook, name='whatsapp-webhook'),
    path("send/", WhatsAppMessageAPI.as_view(), name="whatsapp-send"),
]