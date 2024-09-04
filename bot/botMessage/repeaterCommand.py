from .botMessage import BotMessage
from telebot import types
from bot import bot
from . import menu
import repeater

class ChapterAddition(BotMessage):
  def __init__(self, chat):
    super().__init__(chat)
    self.__stage = 0
    self.__chapter_name = ''
    self.__chapter_description = ''
    bot.send_message(self.chat, 'Введите имя для нового раздела')

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    if self.__stage == 0:
      self.__chapter_name = user_input
      bot.send_message(self.chat, 'Введите описание для нового раздела')
      self.__stage = 1
    elif self.__stage == 1:
      try:
        repeater.add_chapter(self.__chapter_name, user_input)
      except repeater.ChapterError as exc:
        bot.send_message(self.chat, f'ошибка создания раздела: {exc}')
      except repeater.CorrectnessError as exc:
        bot.send_message(self.chat, f'имя некорректно: {exc}')
      else:
        bot.send_message(self.chat,
                         f'раздел {self.__chapter_name} успешно создан')
      finally:
        return menu.menuMessage(self.chat)

  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    pass

###################################################33#########################
###################################################33#########################

class ChapterChanging(BotMessage):
  def __init__(self, chat):
    super().__init__(chat)
    self.__stage = 0
    #stages: 0) name 1) commandSelection
    #2) name 3) description 4) join 5) delete
    self.__chapter_name = ''
    bot.send_message(self.chat, 'Введите название раздела')

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    if self.__stage == 0:
      self.__chapter_name = user_input
      if repeater.chapter_exist(user_input):
        self.sendActive('выберите действие:',
                        self.get_command_selection_markup())
        self.__stage = 1
        self.__chapter_name = user_input
      else:
        bot.send_message(self.chat, 'раздел не найден')
        return menu.menuMessage(self.chat)

    elif self.__stage == 2:
      return self.change_name(user_input)
    elif self.__stage == 3:
      return self.change_description(user_input)
    elif self.__stage == 4:
      return self.join(user_input)

  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    if callback == 'change_name':
      self.sendActive('введите новое имя раздела')
      self.__stage = 2
    elif callback == 'change_description':
      bot.send_message(self.chat, 'старое описание раздела:\n\n' +
                       repeater.get_description_of_chapter(self.__chapter_name))
      self.sendActive('введите новое описание раздела')
      self.__stage = 3
    elif callback == 'join':
      self.sendActive('введите имя второго раздела')
      self.__stage = 4
    elif callback == 'delete':
      return self.delete_chapter()


  def change_name(self, new_name:str):
    try:
      repeater.change_name_of_chapter(self.__chapter_name, new_name)
    except repeater.ChapterError as exc:
      bot.error(self.chat, f'ошибка переименования раздела: {exc}')
    except repeater.CorrectnessError as exc:
      bot.error(self.chat, f'имя некорректно: {exc}')
    else:
      bot.send_message(self.chat,
                       f'раздел "{self.__chapter_name}" успешно переименован '
                       f'как "{new_name}"')
    finally:
      return menu.menuMessage(self.chat)
  def change_description(self, new_description):
    try:
      repeater.change_description_of_chapter(self.__chapter_name, new_description)
    except repeater.ChapterError as exc:
      bot.error(self.chat, f'ошибка изменения раздела: {exc}')
    else:
      bot.send_message(self.chat,
                       f'описание раздела изменено')
    finally:
      return menu.menuMessage(self.chat)

  def join(self, second_chapter):
    """объединить разделы"""
    try:
      bot.send_message(self.chat, 'функционал в разработке')
      #repeater.join(self.__chapter_name, second_chapter)
    except repeater.ChapterError as exc:
      bot.error(self.chat, f'ошибка объединения разделов: {exc}')
    except repeater.CorrectnessError as exc:
      bot.error(self.chat, f'имя некорректно: {exc}')
    else:
      bot.send_message(self.chat,
                       f'разделы успешно объединены')
    finally:
      return menu.menuMessage(self.chat)
    pass

  def delete_chapter(self):
    try:
      repeater.del_chapter(self.__chapter_name)
    except repeater.ChapterError as exc:
      bot.error(self.chat, f'ошибка изменения раздела: {exc}')
    else:
      bot.send_message(self.chat,
                       f'раздел {self.__chapter_name} успешно удалён')
    finally:
      return menu.menuMessage(self.chat)

  def get_command_selection_markup(self):
    """получить меню действий"""
    markup = types.InlineKeyboardMarkup()

    add_chapter = types.InlineKeyboardButton(
      'переименовать', callback_data='change_name')
    change_chapter = types.InlineKeyboardButton(
      'изменить описание', callback_data='change_description')
    markup.row(add_chapter, change_chapter)
    add_topic = types.InlineKeyboardButton(
      'объединить с', callback_data='join')
    change_topic = types.InlineKeyboardButton(
      'удалить раздел', callback_data='delete')
    markup.row(add_topic, change_topic)
    return markup

  ###################################################33#########################
  ###################################################33#########################
  ###################################################33#########################
  ###################################################33#########################
  ###################################################33#########################
  ###################################################33#########################

###################################################33#########################
###################################################33#########################

class TopicAddition(BotMessage):
  def __init__(self, chat):
    super().__init__(chat)
    self.__stage = 0
    self.__topic_name = ''
    bot.send_message(self.chat, 'Введите название темы')

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    if self.__stage == 0:
      self.__topic_name = user_input
      bot.send_message(self.chat, 'Введите название раздела')
      self.__stage = 1
    elif self.__stage == 1:
      try:
        repeater.add_topic(self.__topic_name, user_input)
      except (repeater.TopicError, repeater.TopicError) as exc:
        bot.send_message(self.chat, f'Ошибка создания темы: {exc}')
        return menu.menuMessage(self.chat)
      except repeater.CorrectnessError as exc:
        bot.send_message(self.chat, f'имя некорректно: {exc}')
        return menu.menuMessage(self.chat)
      else:
        bot.send_message(self.chat,
                         f'тема "{self.__topic_name}" успешно создана'
                         f'\n\nвведите текст темы')
        self.__stage = 2
    elif self.__stage == 2:
      try:
        repeater.change_note_of_topic(self.__topic_name, user_input)
      except repeater.TopicError as exc:
        bot.error(self.chat, f'ошибка ввода описания: {exc}')
      finally:
        return menu.menuMessage(self.chat)
  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    pass

###################################################33#########################
###################################################33#########################

class TopicChanging(BotMessage):
  def __init__(self, chat):
    super().__init__(chat)
    self.__stage = 0
    #stages: 0) name 1) commandSelection
    #2) name 3) chapter 4) note 5) double 6) delete
    self.__topic_name = ''
    bot.send_message(self.chat, 'Введите название темы')

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    if self.__stage == 0:
      self.__topic_name = user_input
      if repeater.topic_exist(user_input):
        self.sendActive('выберите действие:',
                        self.get_command_selection_markup())
        self.__stage = 'commandSelection'
        self.__chapter_name = user_input
      else:
        bot.send_message(self.chat, 'тема не найдена')
        return menu.menuMessage(self.chat)

    elif self.__stage == 'name':
      return self.change_name(user_input)
    elif self.__stage == 'chapter':
      return self.change_chapter(user_input)
    elif self.__stage == 'note':
      return self.change_note(user_input)
    elif self.__stage == 'duplicate':
      return self.duplicate(user_input)
    elif self.__stage == 'delete':
      return self.delete_topic()

  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    if callback == 'name':
      self.sendActive('введите новое имя темы')
      self.__stage = 'name'
    elif callback == 'chapter':
      self.sendActive('введите имя второго раздела')
      self.__stage = 'chapter'
    elif callback == 'duplicate':
      self.sendActive('введите название дубля')
      self.__stage = 'duplicate'
    elif callback == 'note':
      bot.send_message(self.chat, 'старый текст:\n\n' +
                       repeater.get_note_of_topic(self.__topic_name))
      self.sendActive('введите новый текст темы')
      self.__stage = 'note'
    elif callback == 'delete':
      return self.delete_topic()


  def change_name(self, new_name:str):
    try:
      repeater.change_name_of_topic(self.__chapter_name, new_name)
    except repeater.TopicError as exc:
      bot.error(self.chat, f'ошибка переименования темы: {exc}')
    except repeater.CorrectnessError as exc:
      bot.error(self.chat, f'имя некорректно: {exc}')
    else:
      bot.send_message(self.chat,
                       f'тема "{self.__chapter_name}" успешно переименована '
                       f'как "{new_name}"')
    finally:
      return menu.menuMessage(self.chat)

  def change_chapter(self, new_name:str):
    try:
      repeater.change_chapter_of_topic(self.__chapter_name, new_name)
    except (repeater.TopicError, repeater.ChapterError) as exc:
      bot.error(self.chat, f'раздел не найден: {exc}')
    except repeater.CorrectnessError as exc:
      bot.error(self.chat, f'имя некорректно: {exc}')
    else:
      bot.send_message(self.chat,
                       f'тема "{self.__chapter_name}" успешно перемещена в '
                       f'раздел "{new_name}"')
    finally:
      return menu.menuMessage(self.chat)

  def duplicate(self, new_name:str):
    try:
      repeater.duplicate_topic(self.__chapter_name, new_name)
    except repeater.TopicError as exc:
      bot.error(self.chat, f'ошибка дублирования: {exc}')
    except repeater.CorrectnessError as exc:
      bot.error(self.chat, f'имя некорректно: {exc}')
    else:
      bot.send_message(self.chat,
                       f'тема "{self.__chapter_name}" успешно дублирована '
                       f'как "{new_name}"')
    finally:
      return menu.menuMessage(self.chat)

  def change_note(self, new_note):
    try:
      repeater.change_note_of_topic(self.__chapter_name, new_note)
    except repeater.TopicError as exc:
      bot.error(self.chat, f'ошибка изменения темы: {exc}')
    else:
      bot.send_message(self.chat,
                       f'текст темы изменён')
    finally:
      return menu.menuMessage(self.chat)

  def delete_topic(self):
    try:
      repeater.del_topic(self.__chapter_name)
    except repeater.TopicError as exc:
      bot.error(self.chat, f'ошибка удаления темы: {exc}')
    else:
      bot.send_message(self.chat,
                       f'тема "{self.__chapter_name}" успешно удалена')
    finally:
      return menu.menuMessage(self.chat)

  def get_command_selection_markup(self):
    """получить меню действий"""
    markup = types.InlineKeyboardMarkup()

    add_chapter = types.InlineKeyboardButton(
      'переименовать', callback_data='name')
    add_chapter = types.InlineKeyboardButton(
      'сменить раздел', callback_data='chapter')
    change_chapter = types.InlineKeyboardButton(
      'изменить текст', callback_data='note')
    markup.row(add_chapter, change_chapter)
    add_topic = types.InlineKeyboardButton(
      'дублировать', callback_data='duplicate')
    change_topic = types.InlineKeyboardButton(
      'удалить', callback_data='delete')
    markup.row(add_topic, change_topic)
    return markup

  ###################################################33#########################
  ###################################################33#########################


class ListOfTopicsInChapterPrinting(BotMessage):
  def __init__(self, chat):
    super().__init__(chat)
    bot.send_message(self.chat, 'Введите название раздела')

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    try:
      self.printList(user_input)
    except repeater.ChapterError as exc:
      bot.send_message(self.chat, f'раздел не найден: {exc}')
    except repeater.TopicError as exc:
      bot.send_message(self.chat, f'ошибка: : {exc}')
    finally:
      return menu.menuMessage(self.chat)
  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    pass

  def printList(self, chapter):
    counter = 1
    text = f'список тем в разделе {chapter}:\n'
    t_list = repeater.topics_from_chapter(chapter)
    for name in t_list:
      topic = (f'{counter}) {name}. '
               f'Изучена {repeater.get_date_of_study(name).strftime("%d.%m.%Y")} '
               f'Повторена {repeater.get_last_repeat_date(name).strftime("%d.%m.%Y")}\n')
      text = text + topic
      counter += 1
    bot.send_message(self.chat, text)

  ###################################################33#########################
  ###################################################33#########################

class TopicRepeating(BotMessage):
  def __init__(self, chat):
    super().__init__(chat)
    self.__stage = 0
    bot.send_message(self.chat, 'Введите название темы')

  def handle_answer(self, user_input):
    """обработать пользовательский ввод"""
    if self.__stage == 0:
      try:
        self.send_topic(user_input)
      except repeater.TopicError as exc:
        bot.send_message(self.chat, f'тема не найдена: {exc}')
        return menu.menuMessage(self.chat)
      else:
        self.__stage = 1
  def handle_button_callback(self, callback:str):
    """обработать нажатие кнопки"""
    if callback == 'repeat':
      try:
        repeater.record_repeat(self.topic_name)
      except repeater.TopicError:
        bot.send_message(self.chat, 'досрочное повторение')
      finally:
        return menu.menuMessage(self.chat)
    if callback == 'cancel':
      bot.send_message('отмена')
      return menu.menuMessage(self.chat)
  def send_topic(self, name):
    self.topic_name = name
    note = repeater.get_note_of_topic(name)
    markup = types.InlineKeyboardMarkup()

    repeat = types.InlineKeyboardButton(
      'отметить повторение', callback_data='repeat')
    cancel = types.InlineKeyboardButton(
      'отмена', callback_data='cancel')
    markup.row(repeat, cancel)
    self.sendActive(f'{name}:\n{note}', markup)


  ###################################################33#########################
  ###################################################33#########################