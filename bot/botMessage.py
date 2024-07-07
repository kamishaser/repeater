"""реализация классов сообщений от бота"""
from .stage import STAGES
from telebot import TeleBot
from telebot import types


class BotMessage:
    """базовый класс сообщения от бота"""

    def __init__(self, chat):
        self.chat = chat


    def handle_button_callback(self, callback:str):
        pass

    def handle_answer(self, user_input):
        pass

