from rest_framework import serializers

class WhatsAppMessageSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=20,
        required=True,
        help_text="Recipient's phone number (without country code, e.g., '1234567890')",
    )
    message = serializers.CharField(
        required=False,
        help_text="Required for text messages",
    )
    message_type = serializers.ChoiceField(
        choices=["text", "image", "template"],
        default="text",
        help_text="Type of WhatsApp message",
    )
    image_url = serializers.URLField(
        required=False,
        help_text="Required if message_type='image'",
    )
    template_name = serializers.CharField(
        required=False,
        help_text="Required if message_type='template'",
    )
    caption = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional caption for media messages",
    )