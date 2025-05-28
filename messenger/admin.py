from django.contrib import admin
from .models import SocialMediaUser, Conversation, ChatMessage

@admin.register(SocialMediaUser)
class SocialMediaUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'social_media_id', 'created_at', 'updated_at')
    search_fields = ('name', 'social_media_id')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'created_at', 'updated_at')
    list_filter = ('channel', 'created_at', 'updated_at')
    search_fields = ('user__name', 'user__social_media_id')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'truncated_message', 'is_read', 'sender', 'created_at', 'updated_at')
    list_filter = ('sender', 'is_read', 'created_at')
    search_fields = ('message', 'conversation__user__name')
    readonly_fields = ('created_at',)
    
    def truncated_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    truncated_message.short_description = 'Message' # type: ignore[attr-defined]






# from django.contrib import admin
# from .models import FacebookUser, ChatMessage
# from django.utils.html import format_html
# from django.urls import reverse

# @admin.register(FacebookUser)
# class FacebookUserAdmin(admin.ModelAdmin):
#     list_display = ('fb_id', 'name', 'created_at', 'updated_at', 'message_count', 'view_chats_link')
#     search_fields = ('fb_id', 'name')
#     readonly_fields = ('created_at', 'updated_at')

#     def message_count(self, obj):
#         return obj.messages.count()
#     message_count.short_description = 'Messages'  # type: ignore[attr-defined]

#     def view_chats_link(self, obj):
#         url = reverse('admin:messenger_chatmessage_changelist') + f'?user__id__exact={obj.id}'
#         return format_html('<a href="{}">View Chats</a>', url)
#     view_chats_link.short_description = 'Chats'  # type: ignore[attr-defined]

# @admin.register(ChatMessage)
# class ChatMessageAdmin(admin.ModelAdmin):
#     list_display = ('truncated_message', 'user', 'is_from_user', 'created_at')
#     list_filter = ('is_from_user', 'created_at')
#     search_fields = ('message', 'user__fb_id')

#     def truncated_message(self, obj):
#         return obj.message[:50]
#     truncated_message.short_description = 'Message'  # type: ignore[attr-defined]

#     def is_from_user_display(self, obj):
#         return 'User' if obj.is_from_user else 'Bot'
#     is_from_user_display.short_description = 'Type'  # type: ignore[attr-defined]