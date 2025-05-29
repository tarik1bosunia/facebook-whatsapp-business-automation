import logging
from typing import Dict

from chatbot.utils import ChatBotUtil
from messaging.services import whatsapp_service, conversation_service
from messaging.models import SocialMediaUser, Conversation, ChatMessage

logger = logging.getLogger(__name__)


class TextMessageHandler:
    def handle(self, message: Dict, sender: str, message_type: str):
        """Process incoming text messages and store in database"""
        text = message['text']['body']
        logger.info(f"New text message from {sender}: {text}")

        # Get or create the user
        user, created = SocialMediaUser.objects.get_or_create(
            social_media_id=sender,
            defaults={
                'name': sender  # You might want to get actual name from message if available
            }
        )

        # Get or create the conversation
        conversation, created = Conversation.objects.get_or_create(
            user=user,
            channel='whatsapp',
            defaults={
                'auto_reply': True  # Default to auto-reply enabled
            }
        )

        # Store the incoming message
        ChatMessage.objects.create(
            conversation=conversation,
            sender='customer',
            message=text,
            is_read=False
        )


        # ================= AUTO REPLY ====================
        if conversation.auto_reply:
            gemini_response = ChatBotUtil.chat_with_gemini(prompt=text)

            # Send the response

            whatsapp_service.WhatsAppService().send_text_message(
                phone_number=sender,
                message=gemini_response.text,
            )

            # Save bot response
            conversation_service.save_message(
                conversation=conversation,
                message=gemini_response.text,
                sender='ai',
                # is_read=True
            )
        # ================= AUTO REPLY ====================


        # Store the outgoing response message
        # ChatMessage.objects.create(
        #     conversation=conversation,
        #     sender='business',
        #     message=response_text,
        #     is_read=True
        # )

