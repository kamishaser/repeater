"""реализация классов сообщений от бота"""
import telebot.types
from telebot import TeleBot
from telebot import types
from .. import bot
import repeater


class Dialog:
    """базовый класс сообщения от бота"""

    def __init__(self, chat):
        self.chat = chat
        self.message_list = []


    def handle_button_callback(self, callback:str):
        """обработать нажатие кнопки"""
        pass

    def handle_answer(self, user_input):
        """обработать пользовательский ввод"""
        pass

    def handle_document(self, document: telebot.types.Document):
        """обработать пользовательский документ"""
        pass

    def send_message(self, text, markup = None):
        """вывести активное сообщение"""
        if len(self.message_list) > 0:
            bot.delete_markup(self.message_list[-1])#удаление неактуальных кнопок
        self.message_list.append(bot.send_message(self.chat, text, markup))

    def setPressedButtonValue(self, text, message = None):
        """добавление названия нажатой кнопки в текст сообщения"""
        if message is None:
            message = self.message_list[-1]
        bot.edit_message_text(message, f'\n-> {text}', True)

    def deactivate_markup(self):
        """удаления значения последней нажатой кнопки"""
        if len(self.message_list) > 0:
            bot.delete_markup(self.message_list[-1])#удаление неактуальных кнопок

    def get_tip_on_choice_topic_to_repeat(self) -> telebot.types.ReplyKeyboardMarkup:
        """список кнопок - вариантов выбора темы для повторения"""
        repeater.handler.topics_to_repeat()
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        counter = 0
        topics = repeater.topics_to_repeat()
        row = []
        for topic in topics:
            row.append(telebot.types.KeyboardButton(topic))
            counter += 1
            if counter > 5:
                break
        markup.add(*row)
        return markup

    def get_tip_on_choice_chapter(self) -> telebot.types.ReplyKeyboardMarkup:
        """список кнопок - вариантов выбора раздела"""
        repeater.handler.topics_to_repeat()
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        counter = 0
        topics = repeater.all_chapters()
        row = []
        for topic in topics:
            row.append(telebot.types.KeyboardButton(topic))
            counter += 1
            if counter > 5:
                break
        markup.add(*row)
        return markup







