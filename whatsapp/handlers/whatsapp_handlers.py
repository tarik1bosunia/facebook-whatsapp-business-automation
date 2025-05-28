import json
import logging
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.conf import settings
from typing import Dict, Optional
from messenger.exceptions import WebhookVerificationError

logger = logging.getLogger(__name__)


class WhatsAppWebhookHandler:
    def __init__(self, request):
        self.verify_token = settings.WHATSAPP_VERIFY_TOKEN
        self.request = request

    def process_webhook(self):
        print(f"Received webhook request method: {self.request.method}")
        if self.request.method == 'GET':
            return self._handle_verification()
        elif self.request.method == 'POST':
            print(self.request.body)
            return self._handle_incoming_message()
        return HttpResponseForbidden()

    def _handle_verification(self) -> HttpResponse:
        """Verify webhook subscription with Meta"""
        try:
            mode = self.request.GET.get('hub.mode')
            token = self.request.GET.get('hub.verify_token')
            challenge = self.request.GET.get('hub.challenge')

            if mode == 'subscribe' and token == self.verify_token:
                logger.info("Webhook verified successfully")
                return HttpResponse(challenge, content_type='text/plain')
            raise WebhookVerificationError("Verification failed")
        except Exception as e:
            return HttpResponseForbidden(str(e))

    def _handle_incoming_message(self) -> JsonResponse:
        """Process incoming message payload"""
        print("=== REACHED INCOMING MESSAGE HANDLER ===")
        try:
            # Check if request body exists
            if not self.request.body:
                return JsonResponse({"error": "Empty request body"}, status=400)

            data = json.loads(self.request.body)
            logger.debug(f"Incoming webhook data: {data}")

            if data.get('object') != 'whatsapp_business_account':
                return JsonResponse({"error": "Invalid object"}, status=400)

            for entry in data.get('entry', []):
                self._process_entry(entry)

            return JsonResponse({"status": "success"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    def _process_entry(self, entry: Dict):
        """Process each entry in the webhook payload"""
        for change in entry.get('changes', []):
            if change.get('field') == 'messages':
                self._process_message_change(change['value'])

    def _process_message_change(self, message_data: Dict):
        """Route message to appropriate handler"""
        from .message_types import (
            TextMessageHandler,
            MediaMessageHandler,
            TemplateMessageHandler
        )

        try:
            messages = message_data.get('messages', [])
            if not messages:
                logger.warning("No messages in message_data")
                return

            message = messages[0]
            sender = message.get('from')
            message_type = message.get('type')

            if not sender or not message_type:
                logger.warning("Missing sender or message type")
                return

            if message_type == 'text':
                TextMessageHandler().handle(message, sender)
            elif message_type in ('image', 'audio', 'video', 'document'):
                MediaMessageHandler().handle(message, sender, message_type)
            elif message_type == 'template':
                TemplateMessageHandler().handle(message, sender)
            else:
                logger.warning(f"Unsupported message type: {message_type}")

        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}", exc_info=True)