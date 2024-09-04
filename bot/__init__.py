"""пакет bot реализует пользовательский телеграм бот интерфейс для repeater"""
__version__ = '1.0.0'


from . import bot
from . import userChat
import typing
import logging

import logging


logger = logging.getLogger(__name__)

log_handler = logging.FileHandler(f"{__name__}.log", mode='w', encoding='utf-8')
log_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)


