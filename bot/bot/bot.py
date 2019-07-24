import os

from telebot import TeleBot

TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

bot = TeleBot(TOKEN)

bot.remove_webhook()
resp = bot.set_webhook(
    url=WEBHOOK_URL, certificate=open('/ssl/ssl_cert.pem', 'r'))
