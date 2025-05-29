
from rest_framework import serializers
from ..models import Customer, Order
from messaging.models import SocialMediaUser
from django.utils.timezone import localtime


class SocialMediaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaUser
        fields = ['platform', 'avatar_url']


class CustomerSerializer(serializers.ModelSerializer):
    lastOrderDate = serializers.SerializerMethodField()
    channel = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    social_media = SocialMediaUserSerializer(many=True, source='social_media_users')

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'createdAt', 'orders_count',
            'total_spent', 'lastOrderDate', 'status', 'channel', 'avatar',
            'social_media'
        ]
        extra_kwargs = {
            'createdAt': {'source': 'created_at'},
        }

    def get_lastOrderDate(self, obj):
        last_order = obj.orders.order_by('-created_at').first()
        if last_order:
            return localtime(last_order.created_at).strftime("%b %d, %Y")
        return None

    def get_channel(self, obj):
        platforms = set(smu.platform for smu in obj.social_media_users.all())
        if len(platforms) > 1:
            return 'both'
        return platforms.pop() if platforms else 'unknown'

    def get_avatar(self, obj):
        # First try to get avatar from social media accounts
        social_avatar = obj.social_media_users.filter(avatar_url__isnull=False).first()
        if social_avatar:
            return social_avatar.avatar_url

        # Fallback to default avatar based on name
        return f"https://i.pravatar.cc/150?u={obj.name}"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Format the total_spent as float instead of string
        data['total_spent'] = float(data['total_spent'])
        # Format the created_at date
        data['createdAt'] = localtime(instance.created_at).strftime("%Y-%m-%dT%H:%M:%S")
        return data