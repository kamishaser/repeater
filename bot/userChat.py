from .botMessage.dialog import Dialog
from .botMessage.menu import menuMessage
from . import bot
import typing
import logging


class UserChat:
    """класс управляющий взаимодействие с пользователем в одном чате"""
    def __init__(self, chat):
        self.__chat = chat
        self.__active_dialog: typing.Optional[Dialog] = None
        bot.delete_all_messages(chat)
        self.menu()  #главная страница
        logging.getLogger('bot').log(logging.INFO,
                       f'открыт чат (id: {chat.id}) с пользователем {chat.username}')

    def start_dialog(self, dialog):  #ввести активное сообщение
        """ввести активное сообщение

        message - активное сообщение. Внимание! В данном констексте
        сообщением является подкласс BotMessage"""

        if self.__active_dialog:
            self.__active_dialog.deactivate_markup()
        self.__active_dialog = dialog
        pass

    def menu(self):  #главная страница
        """выход на главную страницу"""
        self.start_dialog(menuMessage(self.__chat))

    @property
    def __get_active_bot_message(self) -> typing.Optional[Dialog]:
        """получить активное сообщение"""
        return self.__active_dialog

    def handle_user_command(self, command_text: str):
        """обработать пользовательскую команду"""
        if command_text == '/menu':
            self.menu()
        pass


    def handle_user_text(self, text):
        """обработать пользовательский ввод текста"""
        if self.__active_dialog:  #если есть активное сообщение, обработать ответ
            nm = self.__active_dialog.handle_answer(text)
            if issubclass(type(nm), Dialog): #установить следующее активное сообщение
                self.start_dialog(nm)
            elif not bool(nm):
                self.menu()
        else:
            bot.send_message(self.__chat, 'ошибка. Попробуйте заново')
            self.menu()

    def handle_button(self, message, button_callback):
        """обработка нажатия кнопки"""

        if not self.__active_dialog:
            (logging.getLogger('bot').
             debug(f'callback: {button_callback} не обработан'))
            bot.send_message(self.__chat, 'ошибка. Попробуйте заново')
            self.menu()
            return
        if (self.__active_dialog.message_list[-1].id ==
             message.id):  #если есть активное сообщение, обработать ответ
            nm = self.__active_dialog.handle_button_callback(button_callback)
            (logging.getLogger('bot').
             debug(f'callback: {button_callback} обработан успешно'))
            if issubclass(type(nm), Dialog):
                self.start_dialog(nm)
            elif not bool(nm):
                self.menu()
        else:
            (logging.getLogger('bot').
             debug(f'callback: {button_callback} не обработан'))
            bot.send_message(self.__chat, 'ошибка. Попробуйте заново')
            self.menu()


chats: typing.Dict[typing.Any, UserChat] = dict()
