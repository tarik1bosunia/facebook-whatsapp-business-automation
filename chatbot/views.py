import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from chatbot.utils import ChatBotUtil


# Initialize the OpenAI client
@csrf_exempt
def chat_with_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt")

            if not prompt:
                return JsonResponse({"error": "Prompt is required."}, status=400)

            # Create chat completion
            response = ChatBotUtil.chat_with_gemini(prompt)
            
            print(response.text)

            return JsonResponse({"response": response.text}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
