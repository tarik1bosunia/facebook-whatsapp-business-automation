```
User sends message on FB Page
        ↓
FB Webhook → Django (message received)
        ↓
Django sends user message → GEMINI API
        ↓
GEMINI generates Bangla response
        ↓
Django sends Bangla reply → Facebook Graph API (Messenger)
        ↓
User receives reply on FB Messenger
```

https://youtu.be/5y7Br0Lc0mc


🚧 Prerequisites
Facebook Page

Facebook Developer Account

Facebook App linked to the Page

Web server (e.g., Node.js, Python/Django/Flask, etc.)

Webhook endpoint (public URL via your server or something like ngrok for local testing)

OpenAI API key (or other AI model provider)


# initial setup
- [creating project and apps](./guides/creating_project_and_apps.md)
- [dotenv](./guides/dotenv.md)
- [corsheaders](./guides/corsheaders.md)
- [gemini auto reply of messages from messenger](./guides/geimini.md)

# install request
```sh
pip install requests
```
# [facebook api guide](./guides/facebook_api.md)





