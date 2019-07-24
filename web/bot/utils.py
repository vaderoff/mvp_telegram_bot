from time import time

import requests
from django.conf import settings


def generate_sms_code():
    code = str(time()).split('.')[1][:5]
    return code


def send_sms(phone, text):
    r = requests.post('https://lcab.rfsms.ru/lcabApi/sendSms.php',
                      data={
                          'login': settings.SMS_API_LOGIN,
                          'password': settings.SMS_API_PASSWORD,
                          'txt': text,
                          'to': phone
                      })
    return r.json()


def send_telegram_message(telegram_id, text, next_state=False, markup=None):
    r = requests.post('http://bot:5000/bot/sendMessage',
                      json={
                          'telegram_id': telegram_id,
                          'text': text,
                          'next_state': next_state,
                          'markup': markup
                      })
    return r.json()
