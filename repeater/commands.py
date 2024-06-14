"""набор основных комманд для управления повторителем"""
import datetime

from .topicdata import TopicData, topic_dict
from .chapter import Chapter, chapter_dict
from . import checks
from typing import Optional, Dict


def add_topic(
    name: str, #название темы
    chapter: str, #раздел
    note: str = '', #описание темы
    questions: str = '',#вопросы
    answers: str = '',#ответы
    link_dict: Optional[Dict[str, str]] = None,  # список ссылок
) -> TopicData:
    checks.new_name_of_topic_check(name)
    checks.existence_chapter_check(chapter)
    """Добавление новой темы
    
    name : str - имя темы
    chapter: str - раздел в котором состоит тема
        Дополнительно
    note: str - описание темы
    questions: str - - вопросы по теме
    answers: str - ответы на вопросы по теме
    link_dict: Optional[Dict[str, str]] - словарь ссылок"""

    atr_dict = dict()
    atr_dict['chapter'] = chapter
    atr_dict['note'] = note
    atr_dict['date_of_study'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    atr_dict['repeat_counter'] = 0
    atr_dict['linc_dict'] = link_dict  # необходимо вставить проверку
    atr_dict['questions'] = questions
    atr_dict['answers'] = answers
    atr_dict['last_repeat_date'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

    topic = TopicData(atr_dict)
    topic_dict[name] = topic
    return topic


def change_name_of_topic(old_name: str, new_name: str):
    """изменение названия темы

    old_name - старое имя темы
    new_name - новое имя темы"""

    if old_name == new_name:
        return
    checks.existence_topic_check(old_name)
    checks.new_name_of_topic_check(new_name)
    topic_dict[new_name] = topic_dict[old_name]
    del topic_dict[old_name]


def change_chapter_of_topic(topic_name: str, new_chapter_name: str):
    """изменение раздела темы

    topic_name: str - имя темы
    new_chapter_name: str - новое имя раздела"""
    checks.existence_topic_check(topic_name)
    checks.existence_chapter_check(new_chapter_name)
    topic_dict[topic_name].chapter = new_chapter_name


def change_note_of_topic(name: str, note: str):
    """изменение записей по теме

    name - имя темы
    note - конспект по теме
    """
    checks.existence_topic_check(name)
    topic_dict[name].note = note


def change_questions_of_topic(name: str, questions: str):
    """изменение вопросов по теме

    name: str - имя темы
    questions: str - вопросы по теме
    """
    checks.existence_topic_check(name)
    topic_dict[name].questions = questions


def change_answers_of_topic(name: str, answers: str):
    """изменение ответов на вопросы по теме

    name: str - имя темы
    answers: str - ответы на вопросы по теме"""
    checks.existence_topic_check(name)
    topic_dict[name].answers = answers


def change_linc_dict_of_topic(name: str, linc_dict: Dict[str, str]):
    """изменение набора ссылок в теме

    name: str - имя темы
    linc_dict - словарь ссылок формата [имя (str), url (str)]
    """
    checks.existence_topic_check(name)
    for key, value in linc_dict.items():
        checks.name_correct_check(name)
    topic_dict[name].link_dict = linc_dict


def add_linc_in_topic(topic_name: str, linc_name: str, linc: str):
    """добавление ссылки в тему

    topic_name: str
    linc_name: str - название ссылки
    linc: str - url - ссылки"""
    checks.existence_topic_check(topic_name)
    checks.name_correct_check(linc_name)
    topic_dict[topic_name].link_dict[linc_name] = linc
    # проверка уникальности ссылки в теме не предусмотренна


def del_topic(name: str):
    """удаление темы

    name: str: имя темы"""
    checks.existence_topic_check(name)
    del topic_dict[name]


def add_chapter(name: str, description: str = ''):
    """добавление нового раздела

    Добавляет описание {description} в раздел по имени {name}"""
    checks.new_name_of_chapter_check(name)
    chapter_dict[name] = Chapter({'description': description})


def change_name_of_chapter(old_name: str, name: str):
    """изменение имени раздела

    Сменяет имя раздела {old_name} на новое {name}
    Затем обновляет поле chapter во всех темах, состоящих в данном разделе"""
    checks.existence_chapter_check(old_name)
    checks.new_name_of_chapter_check(name)
    chapter_dict[name] = chapter_dict[old_name]
    del chapter_dict[old_name]
    for topic in topic_dict.values():
        if topic.chapter == old_name:
            topic.chapter = name

def change_description_of_chapter(name: str, description : str):
    """изменение описания раздела

    Устанавливает описание {description} в раздел {name}"""
    checks.existence_chapter_check(name)
    chapter_dict[name].description = description


def del_chapter(name: str):
    """удаление раздела

    Проверяет наличие тем в разделе {name}
    Если их нет - удаляет раздел, иначе бросает ChapterError """
    checks.existence_chapter_check(name)
    for topic in topic_dict.values():
        if topic.chapter == name:
            raise checks.ChapterError(
                "невозможно удалить раздел, "
                "в котором состоит хотя бы одна тема")
    del chapter_dict[name]


def clear():
    """полная отчистка repeater"""
    chapter_dict.clear()
    topic_dict.clear()
