from ..models import SocialMediaUser, Conversation, ChatMessage

def handle_whatsapp_message(payload):
    entry = payload.get("entry", [])[0]
    changes = entry.get("changes", [])[0]
    messages = changes.get("value", {}).get("messages", [])
    contacts = changes.get("value", {}).get("contacts", [])

    if messages and contacts:
        msg = messages[0]
        contact = contacts[0]

        sender_id = msg["from"]
        sender_name = contact["profile"]["name"]
        message_text = msg["text"]["body"]

        user, _ = SocialMediaUser.objects.get_or_create(
            social_media_id=sender_id,
            defaults={"name": sender_name}
        )

        conversation, _ = Conversation.objects.get_or_create(
            user=user,
            channel="whatsapp"
        )

        ChatMessage.objects.create(
            conversation=conversation,
            sender="customer",
            message=message_text,
            is_read=False
        )
