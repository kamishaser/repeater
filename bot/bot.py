from . import botMessage
from .stage import STAGES
import telebot
import os, sys
import json


def start():
  assert os.path.exists('data/botData.json')
  with open('data/botData.json', 'r') as file:
    bot_data: dict = json.load(file)

  assert bot_data.get('token')
  bot = telebot.TeleBot(bot_data['token'])

  @bot.message_handler(commands=['start', 'help'])
  def command(message):
    bot.send_message(message.chat.id, 'text')

  try:
    bot.polling(none_stop=True)
  except Exception as exc:
    print(exc)