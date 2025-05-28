from rest_framework import serializers
from .models import SocialMediaUser, Conversation, ChatMessage

class SocialMediaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaUser
        fields = ['id', 'social_media_id', 'name', 'profile_pic_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ConversationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    customer = serializers.SerializerMethodField()
    lastMessage = serializers.SerializerMethodField()
    unreadCount = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'customer', 'lastMessage', 'channel', 'unreadCount']

    def get_customer(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'name': user.name,
            'avatar': user.avatar_url
        }

    def get_lastMessage(self, obj):
        last_msg = obj.last_message()
        if last_msg:
            return {
                'text': last_msg.message,
                'time': last_msg.created_at,
                'isRead': last_msg.is_read
            }
        return None

    def get_unreadCount(self, obj):
        return obj.unread_count()

class ChatMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='message')
    time = serializers.DateTimeField(source='updated_at')
    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'time', 'sender']
