import repeater
from .botMessage import BotMessage
from . import repeaterCommand
from telebot import types
from bot import bot


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
      'повторить тему', callback_data='repeat')
    markup.row(topics_to_repeat, choice_topic_to_repeat)
    topics_in_chapter = types.InlineKeyboardButton(
      'список тем в разделе', callback_data='topics_in_chapter')
    chapter_list = types.InlineKeyboardButton(
      'список разделов', callback_data='сhapter_list')
    markup.row(topics_in_chapter, chapter_list)
    self.sendActive('меню', markup)

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    pass

  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    if callback == 'add_chapter':
      return repeaterCommand.ChapterAddition(self.chat)
    if callback == 'change_chapter':
      return repeaterCommand.ChapterChanging(self.chat)
    if callback == 'add_topic':
      return repeaterCommand.TopicAddition(self.chat)
    if callback == 'change_topic':
      return repeaterCommand.TopicChanging(self.chat)
    if callback == 'topics_in_chapter':
      return repeaterCommand.ListOfTopicsInChapterPrinting(self.chat)
    if callback == 'repeat':
      return repeaterCommand.TopicRepeating(self.chat)
    if callback == 'сhapter_list':
      return self.list_of_all_chapters()
    if callback == 'topics_to_repeat':
      return self.list_of_topics_to_repeat()

    pass

  def list_of_all_chapters(self):
    ch_list = repeater.all_chapters()
    text = "список всех разделов:\n"
    counter = 1
    for name in ch_list:
      chapter = (f'{counter}) {name}  '
                 f'{repeater.number_of_topics_in_chapter(name)} т.\n'
                 f'{repeater.get_description_of_chapter(name)}\n')
      counter += 1
      text += chapter
    bot.send_message(self.chat, text)
    return menuMessage(self.chat)

  def list_of_topics_to_repeat(self):
    ch_list = repeater.topics_to_repeat()
    text = "тем для повторения:\n"
    counter = 1
    for name in ch_list:
      chapter = (f'{counter}) {name}  '
                f'Изучена {repeater.get_date_of_study(name).strftime("%d.%m.%Y")} '
                f'Повторена {repeater.get_last_repeat_date(name).strftime("%d.%m.%Y")}\n')
      counter += 1
      text += chapter
    bot.send_message(self.chat, text)
    return menuMessage(self.chat)

