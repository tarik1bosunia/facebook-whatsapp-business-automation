import logging
from typing import Dict

from ...services import whatsapp_service

logger = logging.getLogger(__name__)

class TextMessageHandler:
    def handle(self, message: Dict, sender: str):
        """Process incoming text messages"""
        text = message['text']['body']
        logger.info(f"New text message from {sender}: {text}")

        # Example: Echo response
        whatsapp_service.WhatsAppService().send_text_message(
            phone_number=sender,
            message=f"You said: {text}"
        )

        # TODO: Add your business logic here