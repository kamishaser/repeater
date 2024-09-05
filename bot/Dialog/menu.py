import repeater
from .dialog import Dialog
from . import repeaterCommand
from . import additionalFunctionality
from telebot import types
from bot import bot


class menuMessage(Dialog):
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
    topics_in_chapter = types.InlineKeyboardButton(
      'список тем в разделе', callback_data='topics_in_chapter')
    markup.row(topics_to_repeat, topics_in_chapter)
    choice_topic_to_repeat = types.InlineKeyboardButton(
      'повторить тему', callback_data='repeat')
    chapter_list = types.InlineKeyboardButton(
      'список разделов', callback_data='сhapter_list')
    other = types.InlineKeyboardButton(
      '...', callback_data='other')
    markup.row(choice_topic_to_repeat, chapter_list, other)
    self.send_message('меню', markup)

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    pass

  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    if callback == 'add_chapter':
      self.setPressedButtonValue('добавить раздел')
      return repeaterCommand.ChapterAddition(self.chat)
    if callback == 'change_chapter':
      self.setPressedButtonValue('изменить раздел')
      return repeaterCommand.ChapterChanging(self.chat)
    if callback == 'add_topic':
      self.setPressedButtonValue('добавить тему')
      return repeaterCommand.TopicAddition(self.chat)
    if callback == 'change_topic':
      self.setPressedButtonValue('изменить тему')
      return repeaterCommand.TopicChanging(self.chat)
    if callback == 'topics_in_chapter':
      self.setPressedButtonValue('список тем в разделе')
      return repeaterCommand.ListOfTopicsInChapterPrinting(self.chat)
    if callback == 'repeat':
      self.setPressedButtonValue('повторить тему')
      return repeaterCommand.TopicRepeating(self.chat)
    if callback == 'сhapter_list':
      self.setPressedButtonValue('список разделов')
      return self.get_list_of_all_chapters()
    if callback == 'topics_to_repeat':
      self.setPressedButtonValue('список тем для повторения')
      return self.get_list_of_topics_to_repeat()
    if callback == 'other':
      self.setPressedButtonValue('...')
      return additionalFunctionality.AdditionalFunctionality(self.chat)


  def get_list_of_all_chapters(self):
    """получение списка всех разделов для для ответа на chapter_list"""
    ch_list = repeater.all_chapters()
    text = "список всех разделов:\n"
    counter = 1
    for name in ch_list:
      chapter = (f'{counter}) {name}  '
                 f'({repeater.number_of_topics_in_chapter(name)} т.)\n'
                 f'{repeater.get_description_of_chapter(name)}\n')
      counter += 1
      text += chapter
    self.send_message(text)
    return menuMessage(self.chat)

  def get_list_of_topics_to_repeat(self):
    """получение списка всех тем, которые пора повторять"""
    ch_list = repeater.topics_to_repeat()
    text = "тем для повторения:\n"
    counter = 1
    for name in ch_list:
      chapter = (f'{counter}) {name}  '
                f'Изучена {repeater.get_date_of_study(name).strftime("%d.%m.%Y")} '
                f'Повторена {repeater.get_last_repeat_date(name).strftime("%d.%m.%Y")}\n')
      counter += 1
      text += chapter
    self.send_message(text)
    return menuMessage(self.chat)

