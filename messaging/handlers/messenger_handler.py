
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse

from chatbot.utils import ChatBotUtil

from .base_handler import BaseHandler
from ..services import user_service, conversation_service
from ..utils import facebook_api

# TODO: need to handle all type of attachments(image, audio, video) also
class MessengerHandler(BaseHandler):
    def __init__(self):
        super().__init__(settings.FB_VERIFY_TOKEN)

    def _handle_incoming_message(self, request):
        try:
            data = json.loads(request.body)
            if data.get('object') == 'page':
                self._process_entries(data.get('entry', []))
                return JsonResponse({'status': 'ok'}, status=200)
            return JsonResponse({'status': 'invalid object'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def _process_entries(self, entries):
        for entry in entries:
            for event in entry.get('messaging', []):
                if event.get('message'):
                    self._handle_message_event(event)
                elif event.get('postback'):
                    self._handle_postback_event(event)

    def _handle_message_event(self, event):
        sender_id = event['sender']['id']
        message = event['message']

        if 'text' in message:
            try:
                user = user_service.get_or_create_user(sender_id)
                conversation = conversation_service.get_or_create_conversation(user)

                # Save incoming message
                user_message = message['text']
                conversation_service.save_message(
                    conversation=conversation,
                    message=user_message,
                    sender='customer'
                )

                # AUTO REPLY
                if conversation.auto_reply:

                    gemini_response = ChatBotUtil.chat_with_gemini(prompt=user_message)

                    facebook_api.send_message(sender_id, gemini_response.text)

                    # Save bot response
                    conversation_service.save_message(
                        conversation=conversation,
                        message=gemini_response.text,
                        sender='ai'
                    )

            except Exception as e:
                print(f"Error processing message: {str(e)}")
                facebook_api.send_message(sender_id, "Sorry, I encountered an error")

    def _handle_postback_event(self, event):
        sender_id = event['sender']['id']
        payload = event['postback']['payload']

        try:
            user= user_service.get_or_create_user(sender_id)
            conversation = conversation_service.get_or_create_conversation(user)

            # Save postback as message
            conversation_service.save_message(
                conversation=conversation,
                message=f"[POSTBACK] {payload}",
                sender='customer'
            )

            response_text = f"You selected: {payload}"
            facebook_api.send_message(sender_id, response_text)

            # Save bot response
            conversation_service.save_message(
                conversation=conversation,
                message=response_text,
                sender='ai'
            )
        except Exception as e:
            print(f"Error processing postback: {str(e)}")
            facebook_api.send_message(sender_id, "Sorry, I couldn't process your selection")