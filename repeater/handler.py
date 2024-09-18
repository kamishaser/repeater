"""внутренний обработчик повторителя"""
from .chapter import Chapter, chapter_dict
from . import checks

import typing
import datetime
from .topicdata import TopicData, topic_dict
from typing import List
from collections import namedtuple

TopicSummary = namedtuple('TopicSummary', [
        'chapter',
        'name',
        'date_of_study',
        'date_of_next_repeat'
    ])  # кортеж для вывода списков тем по критериям

def get_topic_summary(
        name: str, topic: typing.Optional[TopicData] = None) -> TopicSummary:
    checks.topic_exist(name, True)
    """получение сводки по теме"""
    if topic is None:
        topic = topic_dict[name]
    summary = TopicSummary(
        topic.chapter,
        name,
        datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
        checks.next_repeat_date(topic.date_of_study,
                         topic.repeat_counter).strftime('%d.%m.%Y %H:%M'))
    return summary

##############################################################################


def __sort_key(name) -> str:
    """получение ключа сортировки сводок по времени повторения"""
    return datetime.datetime.strftime(
        topic_dict[name].last_repeat_date, '%d.%m.%Y %H:%M')


def record_repeat(name):
    """фиксация повторения темы"""
    checks.topic_exist(name, True)
    topic = topic_dict[name]
    if checks.is_it_time_to_repeat(topic.last_repeat_date, topic.repeat_counter):
        topic.last_repeat_date = datetime.datetime.now()
        topic.repeat_counter = topic.repeat_counter + 1
    else:
        topic.last_repeat_date = datetime.datetime.now()
        raise checks.TopicError("тема повторена раньше времени. Счётчик не увеличился")

##############################################################################


def topics_to_repeat() -> List[str]:
    """вывод списка тем подлежащих повторению"""
    r_list: List[str] = list()
    for name, data in topic_dict.items():
        if checks.is_it_time_to_repeat(data.last_repeat_date, data.repeat_counter):
            r_list.append(name)
    r_list.sort(key=__sort_key)
    return r_list


def topics_from_chapter(chapter_name: str) -> List[str]:
    checks.chapter_exist(chapter_name, True)
    return list(
        map(lambda item: item[0],
            filter(lambda item: (item[1].chapter == chapter_name),
                   topic_dict.items())))


def all_chapters() -> List[str]:
    return list(chapter_dict.keys())
