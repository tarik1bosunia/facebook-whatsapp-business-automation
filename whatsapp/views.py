from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import WhatsAppMessageSerializer
from .services.whatsapp_service import WhatsAppService
import logging

logger = logging.getLogger(__name__)


from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .handlers.whatsapp_handlers import WhatsAppWebhookHandler


@csrf_exempt
def whatsapp_webhook(request):
    handler = WhatsAppWebhookHandler(request)
    return handler.process_webhook()


class WhatsAppMessageAPI(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = WhatsAppMessageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        whatsapp_service = WhatsAppService()

        try:
            if data["message_type"] == "text":
                if not data.get("message"):
                    return Response(
                        {"error": "Message is required for text type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                response = whatsapp_service.send_text_message(
                    data["phone_number"], data["message"]
                )

            elif data["message_type"] == "image":
                if not data.get("image_url"):
                    return Response(
                        {"error": "image_url is required for image type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                response = whatsapp_service.send_image(
                    data["phone_number"], data["image_url"], data.get("caption")
                )

            elif data["message_type"] == "template":
                if not data.get("template_name"):
                    return Response(
                        {"error": "template_name is required for template type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                response = whatsapp_service.send_template(
                    data["phone_number"], data["template_name"]
                )

            return Response(
                {"success": True, "whatsapp_response": response},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            return Response(
                {"error": "Failed to send message", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )