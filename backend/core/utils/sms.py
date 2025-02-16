from django.utils import timezone
from core.models import Reminder
from core.utils import send_custom_email
from django.conf import settings
import logging
import requests
import json

logger = logging.getLogger(__name__)
from django.utils import timezone
from datetime import timedelta


def send_sms(phone_number, message, code="254"):
    api_url = settings.SMS_API_URL
    no = phone_number
    phone_number = phone_number.strip()
    if phone_number.startswith('+'):
        phone_number = phone_number[1:]
    if len(phone_number) > 10:
        no = f"{code}{phone_number[-12:]}"
    elif 9 <= len(phone_number) <= 10:
        no = f"{code}{phone_number[-9:]}"
   
    payload = {
        "SenderId": settings.SMS_SENDER_ID,
        "IsUnicode": True,
        "IsFlash": True,
        "MessageParameters": [
            {"Number": no, "Text": message}
        ],
        "ApiKey": settings.SMS_API_KEY,
        "ClientId": settings.SMS_CLIENT_ID
    }
    json_payload = json.dumps(payload)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.post(api_url, data=json_payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("ErrorCode") == 0:
            for data in response_data.get("Data", []):
                if data.get("MessageErrorCode") == 0:
                    logger.info(f"SMS sent successfully to {data.get('MobileNumber')}")
                else:
                    logger.error(f"Failed to send SMS to {data.get('MobileNumber')}. Error: {data.get('MessageErrorDescription')}")
        else:
            logger.error(f"Failed to send SMS. Error: {response_data.get('ErrorDescription')}")
    else:
        logger.error(f"Failed to send SMS to {phone_number}. Response: {response.text}")
    
    return response
