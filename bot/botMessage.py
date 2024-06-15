"""реализация классов сообщений от бота"""
from .stage import STAGES
from telebot import TeleBot
from telebot import types


class botMessage:
    """базовый класс сообщения от бота"""

    def __init__(self, message, stage):
        self.message = message
        self.stage = stage

    def getStafe(self):
        return self.stage

    def handle_button_callback(self, callback:str):
        pass

    def handle_answer(self, user_message):
        pass

