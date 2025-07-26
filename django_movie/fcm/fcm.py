import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

SERVICE_ACCOUNT_FILE = '/home/d/develosh/osma.academytable.ru/public_html/django_movie/fcm/service-account.json'
PROJECT_ID = '39261319974'  # замените на ваш Firebase ID

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    credentials.refresh(Request())
    return credentials.token

def send_push_notification(token, title, body, mytype, mytypeid):
    access_token = get_access_token()

    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    message = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body,
            },
            "data": {
                "type": mytype,
                "orderId": mytypeid,  # ВАЖНО: строки!
            },
            "apns": {
                "payload": {
                    "aps": {
                        "sound": "default"  # или "custom.caf" если добавил кастомный звук
                    }
                }
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(message))

    return response.status_code, response.json() if response.ok else response.text
