import datetime
from typing import Dict
from typing import Optional
from typing import Union


class TopicData:
    '''класс, описывающий изучаемую тему'''
    chapter: str #раздел
    note: str #конспект по теме
    date_of_study: datetime.datetime #дата изучения темы
    last_repeat_date: datetime.datetime #дата предыдущего повторения темы
    repeat_counter: int = 0 #счётчик повторений
    link_dict: Optional[Dict[str, str]] = None #список ссылок
    questions: str = ''#вопросы
    answers: str = ''#ответы

    def __init__(self, data: Dict[str, Union[str, int, Dict[str, str]]]):
        """конструктор класса по словарю. Предпологается использование при загрузки из json"""
        # необходимо вставить защиту от некорректных типов
        self.chapter = data['chapter']
        self.note = data['note']
        self.date_of_study = datetime.datetime.strptime(
            data['date_of_study'], '%d.%m.%Y %H:%M')
        self.last_repeat_date = datetime.datetime.strptime(
            data['last_repeat_date'], '%d.%m.%Y %H:%M')
        self.repeat_counter = data['repeat_counter']

        self.link_dict = data.get('linc_dict')
        self.questions = data.get('questions')
        self.answers = data.get('answers')

    def save(self, name : Optional[str] = None) -> Dict[str, Union[str, int, Dict[str, str]]]:
        """сохранение в словарь.
        Прдпологается использование для сохранения в json"""
        # необходимо вставить защиту от некорректных типов
        dict1: Dict[str, Union[str, int, Dict[str, str]]] = dict()
        if name is not None:
            dict1['name'] = name
        dict1['chapter'] = self.chapter
        dict1['note'] = self.note
        dict1['date_of_study'] = (
            self.date_of_study.strftime('%d.%m.%Y %H:%M'))
        dict1['last_repeat_date'] = (
            self.last_repeat_date.strftime('%d.%m.%Y %H:%M'))
        dict1['repeat_counter'] = self.repeat_counter
        dict1['linc_dict'] = self.link_dict
        # необходимо вставить проверку
        dict1['questions'] = self.questions
        dict1['answers'] = self.answers

        return dict1


topic_dict: Dict[str, TopicData] = dict()

