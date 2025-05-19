# [Install the Gemini API library](https://ai.google.dev/gemini-api/docs/quickstart?lang=python#install-gemini-library
)
```sh
pip install -q -U google-genai
```
```sh
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "Explain how AI works"}]
    }]
   }'
```

```python 
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```

Hello there! This is Neko. Thank you for reaching out with your question. Django is primarily used to build web applications quickly and efficiently. Here are some of its key applications:\n\n*   **Web application development:** Django's features such as an ORM, routing, templating engine, and security features make it an excellent tool for creating dynamic websites, web portals, and complex web applications.\n\n*   **REST APIs:** Django's flexibility and tools like Django REST Framework (DRF) allow developers to create robust and scalable REST APIs for mobile apps, web services, and other applications that need to communicate over HTTP.\n\n*   **Content management systems (CMS):** The Django admin interface and built-in authentication and authorization features make it a good choice for building CMSs.\n\n*   **E-commerce platforms:** Django can be used to develop e-commerce platforms with features such as product catalogs, shopping carts, user accounts, and payment gateway integration.\n\n*   **Social networking sites:** Django's scalability and ability to handle large amounts of data make it suitable for building social networking sites with features such as user profiles, news feeds, and messaging.\n\nI hope this helps! Please let me know if you have any other questions. I'm always happy to assist!