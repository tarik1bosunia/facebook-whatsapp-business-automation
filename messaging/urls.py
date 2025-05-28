from django.urls import path

from messaging.views.webhooks import messenger_webhook, whatsapp_webhook

urlpatterns = [
    path('webhook/messenger/', messenger_webhook, name='messenger-messaging-webhook'),
    path('webhook/whatsapp/', whatsapp_webhook, name='whatsapp-messaging-webhook'),
]