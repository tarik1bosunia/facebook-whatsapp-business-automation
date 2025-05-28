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

## webhook setup url on facebook messenger
-  https://38ed-103-99-176-51.ngrok-free.app/api/messaging/webhook/messenger/
## webhook setup url on whatsapp
- https://business.facebook.com/latest/settings/system_users?business_id=1786552525544080&selected_user_id=61576759232765
- https://38ed-103-99-176-51.ngrok-free.app/api/messaging/webhook/whatsapp/

# common
- https://38ed-103-99-176-51.ngrok-free.app/api/messaging/webhook/messenger/

# WhatsApp Cloud API Webhook Permissions

To properly receive and manage WhatsApp messages via the Meta (Facebook) Cloud API, you must subscribe to the following webhook events during your Webhook Configuration.

## 1. Required Permissions (Events to Subscribe)

| Permission (Event)         | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `messages`                | Receive incoming messages (text, images, documents, etc.)                   |
| `message_statuses`        | Get delivery updates (sent, delivered, read, failed)                        |
| `message_template_statuses` | Track template message statuses (approved, rejected, etc.)                  |


### 5. Request Required Permissions

| Permission                    | Description                                                    |
|------------------------------|----------------------------------------------------------------|
| `whatsapp_business_management` | Manage WABA and phone numbers                                 |
| `whatsapp_business_messaging`  | Send and receive WhatsApp messages via the Cloud API          |
| `business_management`          | Required only if accessing business portfolio endpoints    

**Steps to request:**

1. Go to **App Dashboard**
2. Click **App Review → Permissions and Features**
3. Click **Request Advanced Access** for the above scopes
4. Provide business use case, privacy policy, and screencast (for production approval)


### Notes:
- These permissions ensure your webhook can handle both **incoming user messages** and **delivery status updates** for messages sent from your system.
- You can configure these events under your [Meta App Dashboard](https://developers.facebook.com/apps/) > Webhooks section.

