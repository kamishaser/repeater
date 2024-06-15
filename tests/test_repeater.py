import datetime
import unittest
import os
import json

import repeater
from repeater.topicdata import topic_dict
from repeater.chapter import chapter_dict
from repeater.commands import clear


class CommandTest(unittest.TestCase):
    """TestCase to testing the commands.py"""
    def test_creation_of_chapters_and_topics(self):
        """Тест создания и разделов и тем

        1) отчистка repeater
        2) создание нового раздела
        3) попытка создания раздела при совпадении имён с п2
        4) попытка создания темы в отсутствующем разделе
        5) создание темы
        6) попытка создания темы при совпадении имён с п5
        7) попытка создания темы с некорректным именем
        """

        #1
        clear()
        #2
        repeater.add_chapter('test_chapter', 'd')
        self.assertTrue(repeater.chapter_exist('test_chapter'),
                        msg='тест создания раздела')
        #3
        self.assertRaises(repeater.ChapterError, repeater.add_chapter,
                          'test_chapter')
                          #msg='запрет на создание разделов с совпадающими именами')
        #4
        self.assertRaises(repeater.ChapterError, repeater.add_topic,
                          'test_topic', 'test_chapter2')
                          #msg='запрет на создание темы в несуществующем разделе')
        #5
        repeater.add_topic('test_topic', 'test_chapter')
        self.assertTrue(repeater.topic_exist('test_topic'),
                        msg='тест создания темы')
        #6
        self.assertRaises(repeater.TopicError, repeater.add_topic,
                          'test_topic', 'test_chapter')
                          #msg='запрет на создание тем с совпадающими именами')
        #7
        self.assertRaises(repeater.CorrectnessError, repeater.add_topic,
                          't', 'test_chapter') #слишком короткое имя
        self.assertRaises(repeater.CorrectnessError, repeater.add_topic,
                          'test' * 60, 'test_chapter') #слишком длинное имя

    def test_deletion(self):
        """Тест удаления разделов и тем

        1) создание эксперементальных тем
        2) попытка удаления раздела в котором есть одна тема
        3) удаление темы
        4) удаление раздела
        5) проверка, что и тема и раздел были успешно удалены
        """

        #1
        clear()
        repeater.add_chapter('test_chapter', 'd')
        repeater.add_topic('test_topic', 'test_chapter', 'd')
        self.assertTrue(
            repeater.chapter_exist('test_chapter') and
            repeater.topic_exist('test_topic'),
            msg='условия проведения теста')

        #2
        self.assertRaises(repeater.ChapterError, repeater.del_chapter,
                          'test_chapter')
        # msg='запрет на удаление непустого раздела')
        #3
        repeater.del_topic('test_topic')
        self.assertFalse(repeater.topic_exist('test_topic'),
                         msg='тест удаления темы')
        #4
        repeater.del_chapter('test_chapter')
        self.assertFalse(repeater.chapter_exist('test_chapter'),
                         msg='тест удаления раздела')

    def test_topic_change(self):
        """Тест изменения темы

        1) создание эксперементальных разделов и тем
        2) изменение имени темы
        2.1) попытка установки имени совпадающего с именем существующей темы
        3) изменение раздела темы
        3.1) попытка установки несуществующего раздела
        4) изменение описания темы
        5) изменение вопросов темы
        6) изменение ответов темы
        7) изменения словаря ссылок темы"""

        #1
        clear()
        repeater.add_chapter('test_chapter1')
        repeater.add_chapter('test_chapter2')
        repeater.add_topic('test_topic1', 'test_chapter1')
        repeater.add_topic('test_topic2', 'test_chapter1')
        #2
        repeater.change_name_of_topic(
            'test_topic1', 'test_topic3')
        self.assertTrue(repeater.topic_exist('test_topic3'))
        self.assertFalse(repeater.topic_exist('test_topic1'))
        #2.1
        self.assertRaises(repeater.TopicError, repeater.change_name_of_topic,
                          'test_topic2', 'test_topic3')
        self.assertRaises(repeater.TopicError, repeater.change_name_of_topic,
                          'test_topic0', 'test_topic4')
        #3
        repeater.change_chapter_of_topic(
            'test_topic2', 'test_chapter2')
        self.assertEqual(
            topic_dict['test_topic2'].chapter, 'test_chapter2')
        #3.1
        self.assertRaises(repeater.ChapterError, repeater.change_chapter_of_topic,
                          'test_topic2', 'test_chapter3')
        #4
        repeater.change_note_of_topic('test_topic2', 'test_note')
        self.assertEqual(topic_dict['test_topic2'].note, 'test_note')
        #5
        repeater.change_questions_of_topic(
            'test_topic2', 'test_question')
        self.assertEqual(
            topic_dict['test_topic2'].questions, 'test_question')
        #6
        repeater.change_answers_of_topic(
            'test_topic2', 'test_answer')
        self.assertEqual(
            topic_dict['test_topic2'].answers, 'test_answer')
        #7
        l_dict = {'google': 'https://www.google.ru/'}
        repeater.change_linc_dict_of_topic(
            'test_topic2', l_dict)
        self.assertEqual(
            topic_dict['test_topic2'].link_dict, l_dict)
        l_dict['yandex'] = 'https://ya.ru/'
        repeater.add_linc_in_topic(
            'test_topic2', 'yandex', 'https://ya.ru/')
        self.assertEqual(
            topic_dict['test_topic2'].link_dict, l_dict)

    def test_chapter_change(self):
        """
        Тест изменения раздела

        1) создание эксперементальных разделов и тем
        2) изменение имени раздела с проверкой изменения разделов в темах
        3) изменение описания раздела
        """
        #1
        clear()
        repeater.add_chapter('test_chapter1')
        repeater.add_chapter('test_chapter2')
        repeater.add_topic('test_topic1', 'test_chapter1')
        #2
        self.assertRaises(repeater.ChapterError, repeater.change_name_of_chapter,
            'test_chapter1', 'test_chapter2') #проверка запрета совпадения имён
        repeater.change_name_of_chapter('test_chapter1', 'test_chapter')
        self.assertTrue(repeater.chapter_exist('test_chapter'))
        self.assertFalse(repeater.chapter_exist('test_chapter1'))
        self.assertEqual(topic_dict['test_topic1'].chapter, 'test_chapter')
        #3
        repeater.change_description_of_chapter(
            'test_chapter', 'test_description')
        self.assertEqual(
            chapter_dict['test_chapter'].description, 'test_description')


class HandlerTest(unittest.TestCase):
    """TestCase to testing the handler.py module

    1) test_topic_summary"""

    def test_repeat_system(self):
        """
        Тест системы повторений

        проверка next_repeat_date и record_repeat на REPEAT_INTERVALS
        """
        clear()
        repeater.add_chapter('test_chapter')
        repeater.add_topic('test_topic', 'test_chapter')

        self.assertFalse(repeater.is_it_time_to_repeat(#проверка, что сейчас рано повторять
            datetime.datetime.now(), 0))
        self.assertTrue(repeater.is_it_time_to_repeat(#проверка, что сейчас пора повторять
            datetime.datetime.now() -
            datetime.timedelta(days=400), 0))

        for number, value in enumerate(repeater.REPEAT_INTERVALS):
            topic_dict['test_topic'].last_repeat_date = (
                    datetime.datetime.now() - datetime.timedelta(days=value-1))
            self.assertRaises(repeater.TopicError,
                              repeater.record_repeat,
                              'test_topic')
            topic_dict['test_topic'].last_repeat_date = (
                    datetime.datetime.now() - datetime.timedelta(days=value+1))
            repeater.record_repeat('test_topic')
            self.assertEqual(topic_dict['test_topic'].repeat_counter, number + 1)

    def test_topic_summary(self):
        """
        Тест сводки по теме

        1) создание условий тестирования
        2) получение сводки и сравнение с ожидаемым результатом
        """
        clear()
        repeater.add_chapter('test_chapter')
        repeater.add_topic(
            'test_topic',
            'test_chapter',
            'test_desctiption',
            'test_questions',
            'test_answers',
        )
        # 2
        summary = repeater.get_topic_summary('test_topic')
        self.assertEqual(summary.chapter, 'test_chapter')
        self.assertEqual(summary.name, 'test_topic')
        self.assertEqual(summary.date_of_study,
                         datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))
        self.assertEqual(summary.date_of_next_repeat,
                         (datetime.datetime.now() +
                          datetime.timedelta(days=1)).
                         strftime('%d.%m.%Y %H:%M'))

    def test_summary_out(self):
        """Тест функций вывода сводок по темам

        1) topics_to_repeat
        2) topics_from_chapter"""

        clear()
        repeater.add_chapter('test_chapter1')
        repeater.add_chapter('test_chapter2')
        repeater.add_topic('test_topic1', 'test_chapter2')
        repeater.add_topic('test_topic2', 'test_chapter1')
        repeater.add_topic('test_topic3', 'test_chapter1')

        #1
        topic_dict['test_topic3'].date_of_study -= datetime.timedelta(days=5)
        topic_dict['test_topic1'].date_of_study -= datetime.timedelta(days=2)
        summary_list = repeater.topics_to_repeat()
        self.assertEqual(len(summary_list), 2)
        self.assertEqual(summary_list[0].name, 'test_topic3')
        self.assertEqual(summary_list[1].name, 'test_topic1')
        #2
        summary_list = repeater.topics_from_chapter('test_chapter1')
        print(summary_list)
        self.assertEqual(len(summary_list), 2)
        self.assertEqual(summary_list[0].name, 'test_topic2')
        self.assertEqual(summary_list[1].name, 'test_topic3')

    def test_chapter_list_out(self):
        """Тест вывода списка разделов"""
        clear()
        repeater.add_chapter('test_chapter1')
        repeater.add_chapter('test_chapter2')
        repeater.add_chapter('test_chapter3')

        self.assertListEqual(repeater.all_chapters(),
                             ['test_chapter1',
                              'test_chapter2',
                              'test_chapter3'])


class DatabaseTest(unittest.TestCase):
    """
    Тестирование базы данных repeater
    """
    @staticmethod
    def gen_test_file():
        clear()
        link_dict = {'google': 'https://www.google.ru/', 'yandex': 'https://ya.ru/'}
        repeater.add_chapter('test_chapter1', 'descripiton1')
        repeater.add_chapter('test_chapter2')
        repeater.add_topic('test_topic1', 'test_chapter1', 'test_note1',
                           'test_question', 'test_answer')
        repeater.change_linc_dict_of_topic('test_topic1', link_dict)
        repeater.add_topic('test_topic2', 'test_chapter1')
        repeater.save('test_data.json')
        clear()

    @staticmethod
    def conflict_data_equal(
            conflict1: repeater.ConflictData, conflict2: repeater.ConflictData) -> bool:
        return (conflict1.name == conflict2.name and
                conflict1.conflict_type == conflict2.conflict_type)

    def test_of_saving_and_loading(self):
        """Тест сохранения и загрузки

        1) создание условий теста
        2) проверка наличия файла
        3) загрузка
        4) проверка, полноты и корректности загрузки"""

        #1
        link_dict = {'google': 'https://www.google.ru/', 'yandex': 'https://ya.ru/'}
        self.gen_test_file()
        #2
        self.assertTrue(os.path.exists('test_data.json'))
        #3
        conflict_list = repeater.load('test_data.json')
        self.assertEqual(len(conflict_list), 0)
        #4
        self.assertEqual(len(chapter_dict), 2)
        self.assertEqual(len(topic_dict), 2)
        self.assertTrue(repeater.chapter_exist('test_chapter1'))
        self.assertTrue(repeater.chapter_exist('test_chapter2'))
        self.assertTrue(repeater.topic_exist('test_topic1'))
        self.assertTrue(repeater.topic_exist('test_topic2'))
        self.assertEqual(
            chapter_dict['test_chapter1'].description, 'descripiton1')
        topic = topic_dict['test_topic1']
        self.assertEqual(topic.chapter, 'test_chapter1')
        self.assertEqual(topic.note, 'test_note1')
        self.assertEqual(topic.questions, 'test_question')
        self.assertEqual(topic.answers, 'test_answer')
        self.assertDictEqual(topic.link_dict, link_dict)

    def test_crash_load(self):
        """Тест ломанной загрузки

        1) создать тестовый файл
        2) попытка загрузки несуществующего файла
        3) сломать тестовый файл, удалив список тем. поймать DatabaseError
        4) cлосать тестовфй файл, уалив имя одной темы, раздел второй и имя второго раздела"""

        #1
        self.gen_test_file()
        #2
        self.assertRaises(repeater.DatabaseError, repeater.load, 'test_data1.json')
        #3
        data = dict()
        with open('test_data.json', 'r') as file:
            data = json.load(file)
        del data['topics']

        with open('test_data.json', 'w') as file:
            json.dump(data, file)
        self.assertRaises(repeater.DatabaseError, repeater.load, 'test_data.json')
        #4
        self.gen_test_file()

        with open('test_data.json', 'r') as file:
            data = json.load(file)

        del data['chapters'][1]['name']
        del data['topics'][0]['name']
        del data['topics'][1]['chapter']

        with open('test_data.json', 'w') as file:
            json.dump(data, file)

        conflict_list = repeater.load('test_data.json')
        self.assertEqual(len(conflict_list), 3)
        expected_conflict_list = [
            repeater.ConflictData('', 2),
            repeater.ConflictData('', 4),
            repeater.ConflictData('test_topic2', 4)
        ]

        self.assertTrue(
            self.conflict_data_equal(conflict_list[0], expected_conflict_list[0]))
        self.assertTrue(
            self.conflict_data_equal(conflict_list[1], expected_conflict_list[1]))
        self.assertTrue(
            self.conflict_data_equal(conflict_list[2], expected_conflict_list[2]))

    def test_conflict(self):
        """Тест конфликтов загрузки

        1) создание файла и создание условий теста
        2) загрузка файла и вывод списка конфликтов
        3) сравнение списка конфликтов с ожидаемым
        4) проверка наличия конфликтного раздела и конфликтной темы"""

        #1
        self.gen_test_file()
        clear()
        repeater.add_chapter('test_chapter1')
        repeater.add_topic('test_topic1', 'test_chapter1')
        #2
        conflict_list = repeater.load('test_data.json')
        #3
        expected_conflict_list = [
            repeater.ConflictData('test_chapter1', 1),
            repeater.ConflictData('test_topic1', 3)
        ]
        self.assertEqual(len(conflict_list), 2)
        self.assertTrue(
            self.conflict_data_equal(conflict_list[0], expected_conflict_list[0]))
        self.assertTrue(
            self.conflict_data_equal(conflict_list[1], expected_conflict_list[1]))
        #4
        self.assertTrue(repeater.chapter_exist("_test_chapter1"))
        self.assertTrue(repeater.topic_exist("_test_topic1"))
        self.assertTrue(repeater.chapter_exist("test_chapter1"))
        self.assertTrue(repeater.topic_exist("test_topic1"))


if __name__ == '__main__':
    unittest.main()
