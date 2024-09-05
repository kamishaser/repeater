"""Модуль dataBase нужен для сохрания и загрузки данных repeater

    save(),
    load(replace) загрузка из файла
"""
import logging

from .topicdata import TopicData, topic_dict
from .chapter import Chapter, chapter_dict
from typing import List, Dict, Optional
import json
import os



class DatabaseError(Exception):
    """ошибка базы данных"""
    pass

class ConflictData:
    """Информация о конфликте

    Описывает информацию о конфликте имён или ошибке,
    возникших при развёртывании загруженных из json файла данных

    fields:
    name: str имя объекта с которым произошла ошибка
    conflictType: int номер типа конфликта:
        0) неизвестная ошибка
        1) совпадение имён разделов
        2) ошибка загрузки раздела
        3) совпадение имён тем
        4) ошибка загрузки темы
        5) не найден раздел, в котором состоит тема"""
    name: str
    conflict_type: int

    def __init__(self, name: str, conflict_type: int):
        self.name = name
        self.conflict_type = conflict_type

def __collect_data():
    """сбор данных в подходящий для сохранения в json формат"""
    dict1 = dict()
    ch_list = list()  # список разделов
    for name, data in chapter_dict.items():
        chapter = data.save(name)
        ch_list.append(chapter)
    t_list = list()  # список тем
    for name, data in topic_dict.items():
        topic = data.save(name)
        t_list.append(topic)
    dict1['chapters'] = ch_list
    dict1['topics'] = t_list
    return dict1


def save(file_name: str = 'data/repeater.json'):
    """сохранение всех данных repeater в json файле"""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(__collect_data(), file, indent=2)


def __deploy_chapters(c_list)\
        -> List[ConflictData]:
    """развёртывание разделов из загруженных из json данных"""
    conflict_list: List[ConflictData] = list()
    for i in c_list:
        name = ''
        try:
            name = i['name']
            if chapter_dict.get(name) is not None:
                conflict_list.append(ConflictData(name, 1))
            else:
                chapter_dict[name] = Chapter(i)
        except KeyError:
            conflict_list.append(ConflictData(name, 2))
    return conflict_list


def __deploy_topics(t_list)\
        -> List[ConflictData]:
    """развёртывание разделов из загруженных из json данных"""
    conflict_list: List[ConflictData] = list()
    for i in t_list:
        name = ''
        try:
            name = i['name']
            if topic_dict.get(name) is not None:
                conflict_list.append(ConflictData(name, 3))
            elif chapter_dict.get(i['chapter']) is None:
                conflict_list.append(ConflictData('name', 5))
            else:
                topic_dict[name] = TopicData(i)
        except KeyError:
            conflict_list.append(ConflictData(name, 4))
    return conflict_list

def __deploy_data(data) -> List[ConflictData]:
    """развёртывание загруженных из json данных"""
    conflict_list: List[ConflictData] = list()

    c_list = data.get('chapters')
    t_list = data.get('topics')

    if not isinstance(c_list, list) or not isinstance(t_list, list):
        raise DatabaseError("ошибка загрузки: некорректный файл")

    conflict_list.extend(__deploy_chapters(c_list))  # развёртывание разделов
    conflict_list.extend(__deploy_topics(t_list))  # развёртывание тем
    return conflict_list

def load(file_name: str = 'data/repeater.json') \
        -> List[ConflictData]:
    """загрузка данных из json файла

    Принимает аргументы: file_name - имя файла загрузки,
    возвращает список конфликтов"""
    if not os.path.exists(file_name):
        raise DatabaseError(f"файла {file_name} не существует")
    with open(file_name, 'r') as file:
        data = json.load(file)
    return __deploy_data(data)

def load_from_json_str(data):
    """загрузка из строки"""
    try:
        dict1 = json.loads(data)
    except Exception as exc: #необходимо добавить более корректное разделение
        logging.getLogger('repeater').error('ошибка загрузки', exc_info=True)
        raise DatabaseError('ошибка считывания json')

    conflicts = __deploy_data(dict1)
    if len(conflicts) == 0:
        return None
    text = "При загрузке возникли конфликты:"
    counter = 1
    for conflict in conflicts:
        con_type = ""
        if conflict.conflict_type == 0:
            con_type = 'неизвестная ошибка'
        elif conflict.conflict_type == 1:
            con_type = 'совпадение имён разделов'
        elif conflict.conflict_type == 2:
            con_type = 'ошибка загрузки раздела'
        elif conflict.conflict_type == 3:
            con_type = 'совпадение имён тем'
        elif conflict.conflict_type == 4:
            con_type = 'ошибка загрузки темы'
        elif conflict.conflict_type == 5:
            con_type = 'не найден раздел, в котором состоит тема'
        text += f'{counter}) {con_type}: "{conflict.name}"\n'
        counter += 1
    return text



