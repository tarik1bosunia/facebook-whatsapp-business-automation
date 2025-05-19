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

# install request
```sh
pip install requests
```

https://youtu.be/IFM3Otvb7So
https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/
https://www.youtube.com/watch?v=dbzzLEHXLck&list=PLGK0jxOchcBcriwOMU9iP1RYGF6nzZUOa




