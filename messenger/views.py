from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .handlers.facebook_handler import FacebookWebhookHandler
from .services import conversation_service
from .utils import facebook_api


@csrf_exempt
def messaging_webhook(request):
    handler = FacebookWebhookHandler(request)
    return handler.process_webhook()


from rest_framework import viewsets, generics, status
from .models import Conversation, ChatMessage
from .serializers import ConversationSerializer, ChatMessageSerializer


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only for now
    queryset = Conversation.objects.all().select_related('user').prefetch_related('messages')
    serializer_class = ConversationSerializer

    # Optional: add filtering by channel or user via query params
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        channel = self.request.query_params.get('channel')

        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if channel:
            queryset = queryset.filter(channel=channel)

        return queryset


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return self.queryset.filter(conversation_id=conversation_id)
        return self.queryset.none()

@api_view(['POST'])
def send_message(request):
    try:
        conversation_id = request.data.get('conversation')
        message = request.data.get('message')

        if not conversation_id or not message:
            return Response({'detail': 'Missing conversation or message.'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.get(id=conversation_id)
        social_media_id = conversation.user.social_media_id

        conversation_service.save_message(
            conversation=conversation,
            message=message,
        )

        facebook_api.send_message(social_media_id, message)

        return Response({'detail': 'Message sent successfully.'}, status=status.HTTP_200_OK)

    except Conversation.DoesNotExist:
        return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# import json
# from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# import requests

# from chatbot.utils import Util
# from messenger.models import ChatMessage, SocialMediaUser

# from rest_framework import generics
# from messenger.serializers import ChatMessageSerializer


# @csrf_exempt
# def messaging_webhook(request):
#     # Handle verification (GET request)
#     if request.method == 'GET':
#         mode = request.GET.get('hub.mode')
#         token = request.GET.get('hub.verify_token')
#         challenge = request.GET.get('hub.challenge')

#         if mode == 'subscribe' and token == settings.FB_VERIFY_TOKEN:
#             print("Webhook verified")
#             return HttpResponse(challenge, content_type='text/plain')
#         return HttpResponseForbidden("Verification failed")

#     # Handle messages (POST request)
#     elif request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             # Make sure this is a page subscription
#             if data.get('object') == 'page':
#                 # Iterate over each entry (there may be multiple if batched)
#                 for entry in data.get('entry', []):
#                     # Get the webhook event
#                     for event in entry.get('messaging', []):
#                         if event.get('message'):    # Message received
#                             handle_message(event)
#                         elif event.get('postback'):   # Postback received
#                             handle_postback(event)

#                 return JsonResponse({'status': 'ok'}, status=200)

#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return JsonResponse({'status': 'error'}, status=500)

#     return HttpResponseForbidden()

# # Handle incoming messages


# def handle_message(event):
#     sender_id = event['sender']['id']
#     message = event['message']

#     print(f"Message from {sender_id}: {message}")

#     # Check if message contains text
#     if 'text' in message:
#         try:
#             # Extract ONLY the text content
#             user_message = message['text']

#             user, _ = SocialMediaUser.objects.get_or_create(fb_id=sender_id)
            
#             # Store user message
#             ChatMessage.objects.create(
#                 user=user,
#                 message=user_message,
#                 is_from_user=True
#             )

            # Get response from Gemini (pass only the text string)
            # gemini_response = Util.chat_with_gemini(prompt=user_message)
            
            # # Store bot reply
            # ChatMessage.objects.create(
            #     user=user,
            #     message=gemini_response.text,
            #     is_from_user=False
            # )

            # # Send the text response back
            # send_message(sender_id, gemini_response.text)

#         except Exception as e:
#             print(f"Gemini processing failed: {e}")
#             send_message(sender_id, "Sorry, I encountered an error. Please try again.")

# # Handle postbacks (e.g., button clicks)
# def handle_postback(event):
#     sender_id = event['sender']['id']
#     payload = event['postback']['payload']
    
#     print(f"Postback from {sender_id}: {payload}")
    
#     reply = f"You clicked: {payload}"
#     send_message(sender_id, reply)

# # Send message back to user
# def send_message(recipient_id, text):
#     url = "https://graph.facebook.com/v22.0/me/messages"
    
#     params = {
#         "access_token": settings.FB_PAGE_ACCESS_TOKEN
#     }
    
#     headers = {
#         "Content-Type": "application/json"
#     }
    
#     data = {
#         "recipient": {"id": recipient_id},
#         "message": {"text": text}
#     }
    
#     response = requests.post(url, params=params, headers=headers, json=data)
    
#     if response.status_code != 200:
#         print(f"Failed to send message: {response.text}")
        
# class ChatHistoryView(generics.ListAPIView):
#     serializer_class = ChatMessageSerializer
#     queryset = ChatMessage.objects.all()  # Default queryset
    
#     def get_queryset(self):
#         """
#         Returns ChatMessage queryset filtered by fb_id
#         """
#         queryset = super().get_queryset()
#         fb_id = self.request.query_params.get('fb_id')
        
#         if fb_id:
#             return queryset.filter(user__fb_id=fb_id).select_related('user')
#         return queryset.none()  # Return empty queryset if no fb_id provided

# class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ChatMessage.objects.all()
#     serializer_class = ChatMessageSerializer        
    
    
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import SocialMediaUser, Conversation, ChatMessage
# from .serializers import SocialMediaUserSerializer, ConversationSerializer, ChatMessageSerializer

# class SocialMediaUserViewSet(viewsets.ModelViewSet):
#     queryset = SocialMediaUser.objects.all()
#     serializer_class = SocialMediaUserSerializer

# class ConversationViewSet(viewsets.ModelViewSet):
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationSerializer

#     @action(detail=True, methods=['get'])
#     def messages(self, request, pk=None):
#         conversation = self.get_object()
#         messages = ChatMessage.objects.filter(conversation=conversation)
#         serializer = ChatMessageSerializer(messages, many=True)
#         return Response(serializer.data)

#     @action(detail=True, methods=['patch'])
#     def mark_as_read(self, request, pk=None):
#         conversation = self.get_object()
#         conversation.is_read = True
#         conversation.save()
#         serializer = self.get_serializer(conversation)
#         return Response(serializer.data)

# class ChatMessageViewSet(viewsets.ModelViewSet):
#     queryset = ChatMessage.objects.all()
#     serializer_class = ChatMessageSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         conversation_id = self.request.query_params.get('conversation_id')
#         if conversation_id:
#             queryset = queryset.filter(conversation_id=conversation_id)
#         return queryset    