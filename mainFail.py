import datetime
import logging

import repeater
#import bot
import typing


import telebot
from telebot import types

bot = telebot.TeleBot('7104572018:AAFYGc8zeHcsJ5Am3dTnjO6VxT36RYW1XD0')


@bot.message_handler(commands=['start', 'help'])
def command(message):
    print(type(message))
    print(message.chat.id)

@bot.message_handler()
def userText(message):
    print(type(message))


def main():
    pass

if __name__ == '__main__':
    main()
bot.polling(none_stop=True)