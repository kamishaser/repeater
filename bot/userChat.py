from . import botMessage
from . import stage
from .botMessage import BotMessage
from .menu import menuMessage
import typing

from telebot import types


class UserChat:

  def __init__(self, chat):
    self.__chat = chat
    self.__active_bot_message: typing.Optional[BotMessage] = None
    activeChat = self
    #стереть всю старую историю чата
    self.menu() #главная страница

  def send_active(self, bot_message: BotMessage): #ввести активное сообщение
    self.__active_bot_message = BotMessage
    pass

  def menu(self): #главная страница
    self.send_active(menuMessage(self.__chat))

  @property
  def active_bot_message(self) -> typing.Optional[BotMessage]:
    return self.__active_bot_message

  def user_command(self, commandText:str):
    pass

  def user_answer(self, text):
    if self.__active_bot_message: #если есть активное сообщение, обработать ответ
      self.__active_bot_message.handle_answer(text)
    else:
      self.user_command('/' + text) #обработать как комманду

  def button(self, button_callback):
    self.__active_bot_message.handle_button_callback(button_callback)


chats: typing.Dict[typing.Any, UserChat] = dict()
