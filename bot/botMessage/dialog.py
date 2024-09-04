"""реализация классов сообщений от бота"""
from telebot import TeleBot
from telebot import types
from .. import bot


class Dialog:
    """базовый класс сообщения от бота"""

    def __init__(self, chat):
        self.chat = chat
        self.message = None


    def handle_button_callback(self, callback:str):
        """обработать нажатие кнопки"""
        pass

    def handle_answer(self, user_input):
        """обработать пользовательский ввод"""
        pass

    def sendActive(self, text, markup = None):
        """вывести активное сообщение"""
        self.message = bot.send_message(self.chat, text, markup)
        print(self.message.id)





