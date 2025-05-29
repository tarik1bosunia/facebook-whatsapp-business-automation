from ..models import Conversation, ChatMessage

def get_or_create_conversation(user):
    conversation, created = Conversation.objects.get_or_create(
        user=user,
        channel='facebook',
        defaults={
            'auto_reply': True  # Default to auto-reply enabled
        }
    )
    return conversation

def save_message(conversation, message, sender='business'):
    return ChatMessage.objects.create(
        conversation=conversation,
        message=message,
        sender=sender,
    )