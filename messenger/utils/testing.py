from ..utils import whatsapp_api

# Initialize the client
wa_client = whatsapp_api.WhatsAppAPI()

# Send a text message
wa_client.send_text_message(
    recipient_phone="15551234567",  # Without country code prefix
    message_text="Hello from our WhatsApp bot!"
)

# Send a template message (for approved templates)
wa_client.send_template_message(
    recipient_phone="15551234567",
    template_name="hello_world",
    language_code="en"
)

# Send an image
wa_client.send_image(
    recipient_phone="15551234567",
    image_url="https://example.com/image.jpg",
    caption="Check out this image!"
)