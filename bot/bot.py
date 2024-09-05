import datetime

import bot.bot
import repeater.database
from . import Dialog
from . import userChat
import telebot
import logging
import os
import json
import requests

__bot : telebot.TeleBot | None = None

def start():
  """запуск бота"""
  global __bot
  assert os.path.exists('data/botData.json')
  with open('data/botData.json', 'r') as file:
    bot_data: dict = json.load(file)

  assert bot_data.get('token')
  __bot = telebot.TeleBot(bot_data['token'])

  @__bot.message_handler(commands=['start'])
  def command(message):
    """обработка ввода команды пользователем"""
    print('start')
    if message.chat.id in userChat.chats:
      userChat.chats[message.chat.id].menu()
    else:
      print('new chat')
      userChat.chats[message.chat.id] = userChat.UserChat(message.chat)

  @__bot.message_handler(content_types=['text'])
  def user_text(message : telebot.types.Message):
    """обработка ввода текста пользователем"""
    if message.chat.id in userChat.chats:
      userChat.chats[message.chat.id].handle_user_text(message.text)
    else:
      print('new chat')
      userChat.chats[message.chat.id] = userChat.UserChat(message.chat)

  @__bot.message_handler(content_types=['document'])
  def user_document(message: telebot.types.Message):
    """обработка отправленных файлов"""
    logging.getLogger('bot').info(
      f'пользователь {message.from_user.username} отправил документ')
    if message.chat.id in userChat.chats:
      userChat.chats[message.chat.id].handle_user_document(message.document)
    else:
      print('new chat')
      userChat.chats[message.chat.id] = userChat.UserChat(message.chat)

  @__bot.callback_query_handler(func=lambda callback: True)
  def callback_message(callback):
    """обработка нажатия на кнопку"""
    if callback.message.chat.id in userChat.chats:
      (userChat.chats[callback.message.chat.id].
       handle_button(callback.message, callback.data))
    else:
      userChat.chats[callback.message.chat.id] = (
        userChat.UserChat(callback.message.chat))

  logging.getLogger('bot').log(logging.INFO, 'бот запущен')
  try:
    __bot.polling(none_stop=True)
  except requests.exceptions.Timeout:
    logging.getLogger('bot').log(logging.CRITICAL, 'потеряно интернет соединение')
  except requests.exceptions.ConnectionError:
    logging.getLogger('bot').log(logging.CRITICAL, 'нет интернета')


def send_message(chat, text, markup = None):
  """отправление сообщения в чат"""
  if __bot:
    if markup is not None:
      return __bot.send_message(chat.id, text, reply_markup=markup)
    else:
      __bot.send_message(chat.id, text)


def delete_message(message):
  """удаление сообщения из чата"""
  if __bot:
    if message:
      __bot.delete_message(message.chat.id, message.message_id)

def delete_markup(message):
  """удалить кнопки в сообщинии"""
  if __bot:
    if message:
      try:
        __bot.edit_message_reply_markup(message.chat.id, message.id, None)
      except telebot.apihelper.ApiException:
        logging.getLogger('bot').error(
          'ApyTelegramException при удалении кнопок')
  pass

def edit_message_text(message, text, add = False):
  if __bot:
    if message:
      try:
        if add:
          text = message.text + text
        __bot.edit_message_text(text, message.chat.id, message.id)
      except telebot.apihelper.ApiException:
        logging.getLogger('bot').error(
          'ApyTelegramException при удалении кнопок')

def delete_all_messages(chat):
  """удалить все сообщения"""
  # messages_to_delete = []
  #
  # messages = __bot.get_chat_history(chat.id)
  # for msg in messages:
  #   messages_to_delete.append(msg.message_id)
  #
  # for msg_id in messages_to_delete:
  #   try:
  #     __bot.delete_message(chat.id, msg_id)
  #   except Exception as e:
  #     logging.getLogger('bot').error('ошибка отчистки чата')
  #   logging.getLogger('bot').info('чат отчищен')
  logging.getLogger('bot').error('функция полной отчистки чата недоработана')


def error(chat, text):
  """зарегистрировать ошибку"""
  send_message(chat, text)
  logging.getLogger('bot').error(text)


def send_data(chat):
  """отправить данные"""
  date = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
  name = 'данные повторителя ' + date + '.json'
  with open('data/repeater.json') as file:
    __bot.send_document(chat_id=chat.id, document= file, visible_file_name=name)

def load_data(data : telebot.types.Document):
  """загрузить данные"""
  file_info = __bot.get_file(data.file_id)
  downloaded_file = __bot.download_file(file_info.file_path)
  return repeater.database.load_from_json_str(downloaded_file)

