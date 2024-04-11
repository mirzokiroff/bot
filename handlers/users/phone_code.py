import random

from loader import db
from twilio.rest import Client


def generate_confirmation_code():
    confirmation_code = ''.join(random.choices('0123456789', k=6))
    return confirmation_code


# Twilio ma'lumotlari
account_sid = 'ACc93368158a47166323e677730e16bc4f'
auth_token = 'eb70f87358cf387a40368c2ad8464711'
twilio_phone_number = '+13343674273'


async def send_confirmation_code(confirmation_code, user_phone_numbers):
    client = Client(account_sid, auth_token)

    for user_phone_number in user_phone_numbers:
        message = client.messages.create(
            body=f"Tasdiqlash kodi: {confirmation_code}",
            from_=twilio_phone_number,
            to=user_phone_number
        )
        print(message.sid)

        print(f"Tasdiqlash kodi foydalanuvchiga yuborildi: {confirmation_code}")
