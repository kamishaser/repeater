"""Пакет repeater реализует систему подразделов и тем
предназначенную для конспектирования и своевременного повторения изучаемого материала """
__version__ = '1.0.1'


from .checks import (
    TopicError, ChapterError, CorrectnessError,
    number_of_topics, number_of_topics_in_chapter,
    number_of_chapter,
    topic_exist, chapter_exist,
    next_repeat_date, is_it_time_to_repeat,
    REPEAT_INTERVALS, MIN_NAME_LENGTH, MAX_NAME_LENGTH)

from .commands import (
    add_topic, del_topic, duplicate_topic,
    change_name_of_topic, change_chapter_of_topic,
    change_questions_of_topic, change_answers_of_topic,
    change_note_of_topic, change_linc_dict_of_topic, add_linc_in_topic,

    add_chapter, del_chapter,
    change_name_of_chapter, change_description_of_chapter,

    get_description_of_chapter,
    get_note_of_topic,
    get_date_of_study, get_last_repeat_date)

from .handler import (TopicSummary, get_topic_summary, record_repeat,
                      topics_to_repeat, topics_from_chapter, all_chapters)

from .database import ConflictData, DatabaseError, save, load



