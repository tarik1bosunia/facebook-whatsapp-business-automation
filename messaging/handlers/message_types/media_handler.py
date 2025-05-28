import logging
from typing import Dict

from messaging.services import whatsapp_service

logger = logging.getLogger(__name__)


class MediaMessageHandler:
    def handle(self, message: Dict, sender: str, media_type: str):
        """Process media messages (images, audio, etc.)"""
        media_id = message[media_type]['id']
        caption = message[media_type].get('caption', 'No caption')

        logger.info(
            f"Received {media_type} from {sender} "
            f"(ID: {media_id}, Caption: {caption})"
        )

        # Example: Acknowledge media receipt
        whatsapp_service.WhatsAppService().send_text_message(
            phone_number=sender,
            message=f"Thanks for the {media_type}! We'll process it soon."
        )