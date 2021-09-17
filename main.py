import os
import time
from datetime import datetime
import requests

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = 'logfile.log'
LOGPATH = os.path.join(ROOT_DIR, FILENAME)
WIKIURL = 'https://en.wikipedia.org/wiki/'

def decorator(delay, path=LOGPATH):
	def pure_decorator(func):
		def wrapper(*args, **kwargs):
			new_function_result = func(*args, **kwargs)

			current_datetime = datetime.now()

			log_str = f'{current_datetime.strftime("%d-%m-%Y %H:%M:%S")}, Запрос к функции: {func.__name__}, Параметры: {args}, {kwargs}\n'

			with open(path, 'a', encoding='utf-8') as file:
				file.write(log_str)
			time.sleep(delay)
			return new_function_result
		return wrapper
	return pure_decorator


class WikiLinks:
	URL = 'https://raw.githubusercontent.com/mledoze/countries/master/countries.json'

	@decorator(2, LOGPATH)
	def get_country(self, country_id):
		response = requests.get(self.URL)
		res_data = response.json()
		return res_data[country_id]['name']['common']

	def __iter__(self):
		self.cursor = 0
		return self

	def __next__(self):
		self.cursor += 1
		country = self.get_country(self.cursor)
		if country is None:
			raise StopIteration
		return country


with open('wikilinks.txt', 'w', encoding='utf-8') as file:
	for country in WikiLinks():
		country_str = country + ' - ' + WIKIURL + country.replace(" ", "_") + '\n'
		file.write(country_str)
