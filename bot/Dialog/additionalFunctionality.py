from .dialog import Dialog
from telebot import types
from bot import  bot
from typing import List
import repeater

class AdditionalFunctionality(Dialog):
	"""диалог дополнительного функционала ... """

	def __init__(self, chat):
		super().__init__(chat)
		self.send_message('дополнительный функционал:',
			self.get_command_selection_markup())
		self.doc_loading = 0
		#self.conflict_list: List[repeater.ConflictData] | None = None

	def handle_answer(self, user_input):
		"""обработать пользовательский ввод"""

	def handle_button_callback(self, callback: str):
		"""обработать нажатие кнопки"""
		if callback == 'print_all':
			self.setPressedButtonValue('показать всё')
			self.print_all()
		elif callback == 'clear':
			self.setPressedButtonValue('удалить всё')
			markup = types.InlineKeyboardMarkup()
			yes = types.InlineKeyboardButton(
				'да', callback_data='ok')
			cancel = types.InlineKeyboardButton(
				'отмена', callback_data='cancel')
			markup.row(yes, cancel)
			self.send_message(
				'Вы уверены, что хотите удалить все ваши данные?', markup)
			return True
		elif callback == 'dump_json':
			self.setPressedButtonValue('выгрузить json')
			bot.send_data(self.chat)
		elif callback == 'load_json':
			self.setPressedButtonValue('загрузить json')
			self.send_message('загрузите json файл с вашими данными. '
							  'Внимание: если есть совпадения в названиях разделов и тем,'
							  'файла с сохранёнными тут, рекомендуется их устранить')
			self.doc_loading = 1
			return True
		elif callback == 'ok':
			self.setPressedButtonValue('да')
			repeater.clear()
			repeater.save()

	def handle_document(self, document: types.Document):
		"""обработать пользовательский документ"""
		if self.doc_loading:
			self.doc_loading = 0
			try:
				result = bot.load_data(document)
				if not result is None:
					self.send_message(result)
			except repeater.DatabaseError as exc:
				bot.error(self.chat, exc)
			else:
				repeater.save()
				self.send_message('документ загружен')

	def print_all(self):
		"""вывести список всех разделов и тем"""
		chapters = repeater.all_chapters()
		c_counter = 1
		text = "список всех тем и разделов:\n"
		for chapter in chapters:
			t_counter = 1
			chapterText = f"{c_counter}) {chapter}:\n"
			topics = repeater.topics_from_chapter(chapter)
			for topic in topics:
				chapterText += f'   {t_counter}) {topic}\n'
				t_counter += 1
			c_counter += 1
			text += chapterText
		self.send_message(text)

	def get_command_selection_markup(self):
		"""получить меню действий"""
		markup = types.InlineKeyboardMarkup()

		print_all = types.InlineKeyboardButton(
			'показать всё', callback_data='print_all')
		clear = types.InlineKeyboardButton(
			'удалить всё', callback_data='clear')
		markup.row(print_all, clear)

		dump_json = types.InlineKeyboardButton(
			'выгрузить json', callback_data='dump_json')
		load_json = types.InlineKeyboardButton(
			'загрузить json', callback_data='load_json')
		markup.row(dump_json, load_json)
		return markup
