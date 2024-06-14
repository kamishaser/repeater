"""набор основных функций проверок repeater"""
import datetime
import random
from .topicdata import TopicData, topic_dict
from .chapter import Chapter, chapter_dict


REPEAT_INTERVALS = (1, 3, 9, 17, 30, 120, 185, 365)
MIN_NAME_LENGTH = 4
MAX_NAME_LENGTH = 60

class TopicError(Exception):
    """ошибка добавления, изменения темы"""
    pass


class ChapterError(Exception):
    """ошибка добавления, изменения раздела"""
    pass


class CorrectnessError(Exception):
    """ошибка корректности строки

    бросается при некорректном имени или url-адресе"""
    pass


def name_correct_check(name: str):
    """Проверка корректности имени name

    Проверяет, что имя является строкой
    Проверяет длину имени от MIN_NAME_LENGTH, до MAX_NAME_LENGTH
    В случае провала бросает CorrectnessError
    """
    if not isinstance(name, str):
        raise CorrectnessError("the name must be a string")
    if len(name) <= MIN_NAME_LENGTH:
        raise CorrectnessError(
            f"the name length must be more than {MIN_NAME_LENGTH}")
    if len(name) >= MAX_NAME_LENGTH:
        raise CorrectnessError(
            f"the name length must be less than {MAX_NAME_LENGTH}")


def new_name_of_topic_check(name: str):
    """
    Проверка названия новой темы

    Проверяет, что темы с таким названием нет
    Проверяет, что название корректно
    В случае провала бросает TopicError
    """
    if name in topic_dict:
        raise TopicError(
            f"тема {name} уже существует. Название должно быть уникальным")
    name_correct_check(name)


def existence_topic_check(name: str):
    """Проверка наличия темы {name}

    В случае отсутствия темы с таким названиет бросает TopicError"""
    if name not in topic_dict:
        raise TopicError(f"темы {name} не существует")


def new_name_of_chapter_check(name: str):
    """Проверка названия нового раздела

    Проверяет, что раздела с таким названием нет
    Проверяет, что название корректно
    В случае провала бросает ChapterError"""
    if name in chapter_dict:
        raise ChapterError(f"раздел {name} уже существует. Название должно быть уникальным")
    name_correct_check(name)


def existence_chapter_check(name: str):
    if name not in chapter_dict or name is None:
        raise ChapterError(f"раздела {name} не существует")



def number_of_topics() -> int:
    """количество тем"""
    return len(topic_dict)


def number_of_chapter() -> int:
    """количество разделов"""
    return len(chapter_dict)


def chapter_exist(name: str) -> bool:
    return chapter_dict.get(name) is not None


def topic_exist(name: str) -> bool:
    return topic_dict.get(name) is not None


def next_repeat_date(
        last_repeat_date: datetime.datetime, repeat_counter: int) -> datetime.datetime:
    """дата следующего повторения темы"""
    return last_repeat_date + datetime.timedelta(
        days=REPEAT_INTERVALS[repeat_counter] if repeat_counter < 7 else 365)


def is_it_time_to_repeat(
        last_repeat_date: datetime.datetime, repeat_counter: int) -> bool:
    """проверка, пора ли повторять тему"""
    return next_repeat_date(last_repeat_date, repeat_counter) < datetime.datetime.now()

