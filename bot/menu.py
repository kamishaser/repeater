from .botMessage import BotMessage
from telebot import types
from . import bot


class menuMessage(BotMessage):
  def __init__(self, chat):
    super().__init__(chat)
    markup = types.InlineKeyboardMarkup()

    add_chapter = types.InlineKeyboardButton(
      'добавить раздел', callback_data='add_chapter')
    change_chapter = types.InlineKeyboardButton(
      'изменить раздел', callback_data='change_chapter')
    markup.row(add_chapter, change_chapter)
    add_topic = types.InlineKeyboardButton(
      'добавить тему', callback_data='add_topic')
    change_topic = types.InlineKeyboardButton(
      'изменить тему', callback_data='change_topic')
    markup.row(add_topic, change_topic)
    topics_to_repeat = types.InlineKeyboardButton(
      'список тем для повторения', callback_data='topics_to_repeat')
    choice_topic_to_repeat = types.InlineKeyboardButton(
      'повторить тему', callback_data='choice_topic_to_repeat')
    markup.row(topics_to_repeat, choice_topic_to_repeat)
    topics_in_chapter = types.InlineKeyboardButton(
      'список тем в разделе', callback_data='topics_in_chapter')
    chapter_list = types.InlineKeyboardButton(
      'список разделов', callback_data='сhapter_list')
    markup.row(topics_in_chapter, chapter_list)

    print('sm')
    bot.send_message(self.chat, 'меню', markup)

  def handle_answer(self, user_input):
    pass






