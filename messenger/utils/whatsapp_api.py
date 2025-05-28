import requests
from django.conf import settings
from requests.exceptions import RequestException


class WhatsAppAPI:
    def __init__(self):
        self.base_url = "https://graph.facebook.com"
        self.api_version = "v22.0"
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN

    def _make_request(self, endpoint, payload):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/{self.api_version}/{self.phone_number_id}/{endpoint}"

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            if hasattr(e, 'response') and e.response:
                print(f"Response content: {e.response.text}")
            raise

    def send_text_message(self, recipient_phone, message_text):
        """
        Send a text message to a WhatsApp user
        Args:
            recipient_phone: Phone number in format 1234567890 (no country code)
            message_text: Text message to send
        """
        # WhatsApp requires phone number in format 1234567890 without '+' or '00'
        endpoint = "messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {
                "preview_url": False,  # Set to True if you want link previews
                "body": message_text
            }
        }
        return self._make_request(endpoint, payload)

    def send_template_message(self, recipient_phone, template_name, language_code="en", components=None):
        """
        Send a template message (for post-auth or pre-approved templates)
        Args:
            recipient_phone: Phone number in format 1234567890
            template_name: Name of your approved template
            language_code: Language code (e.g. "en", "es")
            components: Optional template components
        """
        endpoint = "messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }

        if components:
            payload["template"]["components"] = components

        return self._make_request(endpoint, payload)

    def send_image(self, recipient_phone, image_url, caption=None):
        """
        Send an image message
        Args:
            recipient_phone: Phone number in format 1234567890
            image_url: Publicly accessible URL of the image
            caption: Optional caption text
        """
        endpoint = "messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "image",
            "image": {
                "link": image_url
            }
        }

        if caption:
            payload["image"]["caption"] = caption

        return self._make_request(endpoint, payload)

    def mark_message_as_read(self, message_id):
        """
        Mark a message as read
        Args:
            message_id: ID of the message to mark as read
        """
        endpoint = "messages"
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        return self._make_request(endpoint, payload)