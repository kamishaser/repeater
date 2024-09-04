from .botMessage.botMessage import BotMessage
from .botMessage.menu import menuMessage
from . import bot
import typing
import logging


class UserChat:
    """класс управляющий взаимодействие с пользователем в одном чате"""
    def __init__(self, chat):
        self.__chat = chat
        self.__active_bot_message: typing.Optional[BotMessage] = None
        bot.delete_all_messages(chat)
        self.menu()  #главная страница
        logging.getLogger('bot').log(logging.INFO,
                       f'открыт чат (id: {chat.id}) с пользователем {chat.username}')

    def send_active(self, message: BotMessage):  #ввести активное сообщение
        """ввести активное сообщение

        message - активное сообщение. Внимание! В данном констексте
        сообщением является подкласс BotMessage"""


        assert issubclass(type(message), BotMessage)
        if self.__active_bot_message:
            if self.__active_bot_message.message:
                bot.delete_markup(self.__active_bot_message.message)
        self.__active_bot_message = message
        pass

    def menu(self):  #главная страница
        self.send_active(menuMessage(self.__chat))

    @property
    def active_bot_message(self) -> typing.Optional[BotMessage]:
        return self.__active_bot_message

    def user_command(self, command_text: str):
        if command_text == '/menu':
            self.menu()
        pass


    def user_answer(self, text):
        if self.__active_bot_message:  #если есть активное сообщение, обработать ответ
            nm = self.__active_bot_message.handle_answer(text)
            if nm: #установить следующее активное сообщение
                self.send_active(nm)
        else:
            bot.send_message(self.__chat, 'ошибка. Попробуйте заново')
            self.menu()

    def button(self, message, button_callback):
        """обработка нажатия кнопки"""

        if not self.__active_bot_message:
            (logging.getLogger('bot').
             debug(f'callback: {button_callback} не обработан'))
            bot.send_message(self.__chat, 'ошибка. Попробуйте заново')
            self.menu()
            return
        if (self.__active_bot_message.message.id ==
             message.id):  #если есть активное сообщение, обработать ответ
            nm = self.__active_bot_message.handle_button_callback(button_callback)
            (logging.getLogger('bot').
             debug(f'callback: {button_callback} обработан успешно'))
            if nm is not None:
                self.send_active(nm)
        else:
            (logging.getLogger('bot').
             debug(f'callback: {button_callback} не обработан'))
            bot.send_message(self.__chat, 'ошибка. Попробуйте заново')
            self.menu()


chats: typing.Dict[typing.Any, UserChat] = dict()
