# [Test Facebook Webhook on localhost](https://dashboard.ngrok.com/get-started/setup/windows)
## 1. Install ngrok -> from cmd run as adminstrator
```sh
choco install ngrok
```
## Run the following command to add your authtoken to the default ngrok.yml configuration file.
```sh
ngrok config add-authtoken 2xOQBEl0GXQB2XnCNjKrcidqjsH_sRYMDyxxRwJRnQukNheJ44M
```
##  92ac-103-99-177-138.ngrok-free.app need to add in allowed host
```py
ALLOWED_HOSTS = [
    '92ac-103-99-177-138.ngrok-free.app'
]

```
## 2. Run Django server locally
```sh
python manage.py runserver 8000
```
## 3. Start ngrok on the same port
```sh
ngrok http http://localhost:8000
```
## https://92ac-103-99-177-138.ngrok-free.app -> http://localhost:8000

## webhook setup url on facebook
- https://developers.facebook.com/apps/1405936334088402/webhooks/
- https://c776-103-99-176-48.ngrok-free.app/messenger/webhook/