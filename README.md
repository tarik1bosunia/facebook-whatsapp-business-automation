```
User sends message on FB Page
        ↓
FB Webhook → Django (message received)
        ↓
Django sends user message → ChatGPT API
        ↓
ChatGPT generates Bangla response
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



```sh
django-admin startproject facebook_business_automation
python manage.py startapp facebook
python manage.py startapp chatgpt
```

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'facebook',
    'chatgpt',
]
```


# initial setup
- [dotenv](./guides/dotenv.md)
- [corsheaders](./guides/corsheaders.md)

# install request: testing purpose , i will remove it in future
```sh
pip install requests
```

# need
1. need chatgpt api key where payment done

```sh
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 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" \
  -d '{
    "model": "gpt-4o-mini",
    "store": true,
    "messages": [
      {"role": "user", "content": "write a haiku about ai"}
    ]
  }'
```
https://youtu.be/IFM3Otvb7So
https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/
https://www.youtube.com/watch?v=dbzzLEHXLck&list=PLGK0jxOchcBcriwOMU9iP1RYGF6nzZUOa




