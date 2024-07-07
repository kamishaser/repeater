import datetime
import logging

import repeater
import bot
import atexit

@atexit.register
def end():
    repeater.database.save()

def main():
    repeater.database.load()
    bot.bot.start()
    pass



if __name__ == '__main__':
    main()
#bot.polling(none_stop=True)