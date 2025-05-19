import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from google import genai
from google.genai import types

# Initialize the OpenAI client
client = genai.Client(api_key=settings.GEMINI_API_KEY)
@csrf_exempt
def chat_with_gemini(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt")

            if not prompt:
                return JsonResponse({"error": "Prompt is required."}, status=400)

            # Create chat completion
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                system_instruction="You are a manager. Your name is Neko. You are replying to a customer. You are very polite and friendly. no markdown text just short reply of message",),
                contents=prompt
            )
            print(response.text)

            return JsonResponse({"response": response.text}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
