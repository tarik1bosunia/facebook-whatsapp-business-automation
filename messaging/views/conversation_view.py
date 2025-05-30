from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Conversation, ChatMessage
from ..serializers import ConversationSerializer, ChatMessageSerializer
from ..services import conversation_service, whatsapp_service
from ..utils import facebook_api


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only for now
    queryset = Conversation.objects.all().select_related('user').prefetch_related('messages')
    serializer_class = ConversationSerializer
    pagination_class = None

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
    pagination_class = None

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
            sender='business',
        )
        if conversation.user.platform == 'facebook':
            facebook_api.send_message(social_media_id, message)
        elif conversation.user.platform == 'whatsapp':
            whatsapp_service.WhatsAppService().send_text_message(
                phone_number=social_media_id,
                message=message,
            )


            # whatsapp_api.send_message(social_media_id, message)

        return Response({'detail': 'Message sent successfully.'}, status=status.HTTP_200_OK)

    except Conversation.DoesNotExist:
        return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)