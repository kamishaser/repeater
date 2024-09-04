"""реализация классов сообщений от бота"""
from telebot import TeleBot
from telebot import types
from .. import bot


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







