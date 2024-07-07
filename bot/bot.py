from . import botMessage
from .stage import STAGES
from . import userChat
import telebot
import os
import json

__bot = None
def send_message(chat, text, markup): #отправление сообщения
  if __bot:
    return __bot.send_message(chat.id, text, reply_markup=markup)

def start():
  global __bot
  assert os.path.exists('data/botData.json')
  with open('data/botData.json', 'r') as file:
    bot_data: dict = json.load(file)

  assert bot_data.get('token')
  __bot = telebot.TeleBot(bot_data['token'])

  @__bot.message_handler(commands=['start'])
  def command(message):
    print('start')
    if message.chat.id in userChat.chats:

      userChat.chats[message.chat.id].menu()
    else:
      print('new chat')
      userChat.chats[message.chat.id] = userChat.UserChat(message.chat)

  __bot.polling(none_stop=True)