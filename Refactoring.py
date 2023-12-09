import sublime, sublime_plugin
import re
import time

# Входные данные
# координаты указателя (x, y)
# номер строки
# текущая строка
# выделенный текст - строка
# весь документ
# предыдущая строка

# Задачи
# Извлечь переменную
# Извлечь метод
# последовательное аддитивное выделение: имя функции -> имя функции со всем вызовом -> со следующим вызовом и т.д. Объект -> объект с атрибутом -> со следующим атрибутом или вызовом функции и т.д. Список -> значение списка по ключу и предыдущие цепочки. Словарь -> значение словаря по ключу и предыдущие цепочки.
# обернуть выделенное выражение в вызов функции, метода или в ключ массива


print("Плагин рефакторинга")

class RefactoringExtractVariable(sublime_plugin.TextCommand):
	def run(self, edit):
		self.is_extract = False
		self.edit = edit
		print("Команда извлечь переменную")
		for region in self.view.sel():
			print("проверка выделенного текста")
			if not region.empty():
				# Получаем выделенный текст
				self.selected_text = self.view.substr(region)
				print("выделенный текст", self.selected_text)

				# Получаем позицию курсора и номер строки
				self.cursos_pos = region.begin()
				print("позиция указателя от начала документа", self.cursos_pos)
				self.row, self.col = self.view.rowcol(self.cursos_pos)
				print("номер строки", self.row)
				print("позиция указателя", self.col)

				# Получение содержимого текущей строки
				line_region = self.view.line(self.cursos_pos)
				# print('line_region', line_region)
				self.line_text = self.view.substr(line_region)
				print('содержимое текущей строки', self.line_text)

				# последняя позиция предыдущей строки
				self.line_pos_start = self.cursos_pos - self.col - 1
				print("последняя позиция предыдущей строки", self.line_pos_start)

				# получение содержимого строки выше
				line_region_prev = self.view.line(self.line_pos_start)
				line_text_prev = self.view.substr(line_region_prev)
				print("содержимое предыдущей строки", line_text_prev)

				sublime.active_window().show_input_panel("Извлечь в переменную:", "", lambda text: self.on_done(edit, region, text), None, None)

	def on_done(self, edit, region, input_text):
		# Обработка введенного текста после закрытия всплывающего окна

		# sublime.message_dialog("Вы ввели: " + input_text)

		new_var = input_text

		# новая строка с переменной
		var_assign = new_var + " = " + self.selected_text

		# замена текста (неизвестно, что делает)
		# self.view.replace(edit, region, selected_text)

		# текст до выделения
		text_before_sel = self.line_text[:self.col]
		print('текст до выделения', text_before_sel)

		# количество пробелов в начале строки (табуляция)
		tab_count = len(text_before_sel) - len(text_before_sel.lstrip())
		print('количество пробелов в начале строки', tab_count)

		# Вставить новую переменную
		# self.view.sel().clear()
		# self.view.sel().add(self.cursos_pos)
		self.view.run_command("insert", {"characters": new_var})
		cursor_pos = region.begin()

		# вставка текста (перевод строки + табуляция + присвоение переменной)
		tabs = ' ' * tab_count
		# text_insert = '\n' + tabs + var_assign
		text_insert = '\n' + var_assign
		# self.view.insert(edit, self.line_pos_start, text_insert)
		self.view.sel().clear()
		self.view.sel().add(self.line_pos_start)
		self.view.run_command("insert", {"characters": text_insert})

		# установить курсор в конец вставки
		self.view.sel().clear()
		self.view.sel().add(cursor_pos + len(text_insert) + len(tabs) + len(new_var))			

class ExtractVariableCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("Извлечение имени переменной, вариант от gpt")

		for region in self.view.sel():

			print("проверка выделенного текста")
			if not region.empty():
				# Получаем выделенный текст
				# selected_text = self.view.substr(self.view.sel()[0])
				selected_text = self.view.substr(region)

				print("выделенный текст", selected_text)

				cursor_pos = self.view.sel()[0].begin()

				# Запрашиваем у пользователя имя для новой переменной
				sublime.active_window().show_input_panel('Enter variable name', '', lambda text: self.on_done(edit, region, selected_text, cursor_pos, text), None, None)		

	def on_done(self, edit, region, selected_text, cursor_pos, input_text):
		print("Текст введен", input_text)

		new_variable_name = input_text

		# Формируем новый текст с извлеченной переменной
		new_text = new_variable_name + " = " + selected_text + "\n"

		# Вставляем новый текст в документ
		# self.view.insert(edit, self.view.sel()[0].begin(), new_text)
		self.view.sel().clear()
		self.view.sel().add(cursor_pos)
		self.view.run_command("insert", {"characters": new_text})

		# Заменяем выделенный текст на новую переменную
		self.view.replace(edit, selected_text, new_variable_name)

# class Refactoring(sublime_plugin.EventListener):
# 	def on_text_command(self, view, command_name, args):
# 		print("Прослушивание текстовых команд")
# 		if command_name == "refactoring_extract_variable":
# 			return RefactoringExtractVariable(view)