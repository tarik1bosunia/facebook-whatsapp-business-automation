from rest_framework import serializers
from .models import SocialMediaUser, Conversation, ChatMessage



class SocialMediaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaUser
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    customer = serializers.SerializerMethodField()
    lastMessage = serializers.SerializerMethodField()
    unreadCount = serializers.SerializerMethodField()
    channel = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'customer', 'auto_reply', 'lastMessage', 'channel', 'unreadCount']

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

    def get_channel(self, obj):
        return obj.user.platform

class ChatMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='message')
    time = serializers.DateTimeField(source='updated_at')
    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'time', 'sender']


class AutoReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'auto_reply']
        read_only_fields = ['id']