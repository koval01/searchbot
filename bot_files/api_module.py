import aiohttp, logging, json, string, re
import messages as msg
from random import choice, randint, shuffle
from datetime import datetime
from config import api_host_search, api_key, cx, admins, news_api_key, news_check_words, weather_api_key, default_limit


temp_memory_array = []

async def data_get(question) -> dict:
	"""
	Запит до Google API
	:param question: Текст запитання
	:return: JSON відповідь переведена в словник
	"""
	q = await cleanhtml(question)
	shuffle(api_key)
	for i, e in enumerate(api_key):
		async with aiohttp.request('GET', api_host_search, params={
			"key": api_key[i],
			"cx": cx,
			"q": q,
		}) as response:
			if response.status == 200 and await response.text():
				return json.loads(await response.text())


async def data_prepare(data) -> list:
	array = []
	template_data_error = False
	try:
		if data['searchInformation']['totalResults']:
			try:
				array.append({
					"title": data['context']['title'],
					"SearchTime": data["searchInformation"]["formattedSearchTime"],
					"TotalResults": data["searchInformation"]["formattedTotalResults"],
				})
			except Exception as e:
				logging.error(e)
				template_data_error = True
			if not template_data_error:
				for i, el in enumerate(data["items"]):
					token = await get_random_string()
					array.append([el['title'], 'inline_data:%s' % token])
					temp_memory_array.append([token, el])
				return array
	except Exception as e:
		logging.error(e)


async def search_and_decode_el(token) -> dict:
	for i in temp_memory_array:
		if i[0] == token:
			el = i[1]
			pagemap = True
			try:
				p = el["pagemap"]
			except Exception as e:
				logging.error(e)
				pagemap = False
			array = [
				el["link"],
				el["htmlTitle"],
				el["snippet"].replace('\n', ' '),
			]
			if pagemap:
				img_get = True
				try:
					if p["cse_image"]:
						array.append(p["cse_image"][0]["src"])
				except Exception as e:
					img_get = False
					logging.error(e)
				try:
					if p["cse_thumbnail"] and not img_get:
						array.append(p["cse_thumbnail"][0]["src"])
				except Exception as e:
					logging.error(e)
			return array


async def cleanhtml(raw_html) -> str:
	"""
	Очищуємо строку від HTML тегів
	"""
	return re.sub(re.compile('<.*?>'), '', raw_html)


async def get_random_string(length=12) -> str:
	"""
	Генерация рандомной строки из цифр и букв
	"""
	if length == 0:
		length = randint(12, 20)
	letters = string.ascii_letters + string.digits
	return ''.join(choice(letters) for i in range(length))


async def title_cut(title) -> str:
	"""
	Якщо текст дуже довгий, то скорочуємо його
	:param title: Текст який потрібно перевірити
	:return:
	"""
	title.lstrip()
	title.rstrip()
	title = title.replace('\n', ' ')
	if len(title) > 120:
		title = title[:120]+'...'
	return title


async def check_admin(message) -> bool:
	"""
	Перевірка прав адміністратора
	:rtype: object
	:param message: Message body
	:return: bool result
	"""
	if str(message.from_user.id) in admins:
		return True


async def check_limit(message, db) -> bool:
	"""
	Функція для перевірки вичерпання ліміту пошуків користувача
	:param message: Тіло повідомлення
	:param db: Клас виклику методів SQL Контролера
	:return: bool result
	"""
	u = message.from_user.id
	up = db.update_custom_field
	d = db.subscriber_get_from_user_id(u)[0]
	day = datetime.today().day
	prem = d[9]
	dt = d[7]
	limit = d[8]
	default_max = default_limit

	if dt == day:
		if not prem and limit >= default_max:
			return False
		elif limit >= default_max+prem:
			return False
		else:
			up(u, 'limit_num', 1, 1)
	else:
		up(u, 'limit_day', day)
		up(u, 'limit_num', 0)
	return True


async def news_request(ln) -> dict:
	"""
	Функція запиту до News API
	:param ln: Мовний код
	:return: dict news
	"""
	url = 'https://rapid-art.koval.workers.dev/'
	shuffle(news_api_key)
	cnt = ['ua', 'ru', 'us']
	for i, e in enumerate(news_api_key):
		async with aiohttp.request('GET', url, params={
			"apiKey": news_api_key[i],
			"country": cnt[ln],
			"category": 'general',
		}) as response:
			if response.status == 200 and await response.text():
				data = await response.text()
				return json.loads(data)['articles']


async def weather_request(lat, lon, ln) -> dict:
	"""
	Функція запиту до OpenWeatherMap API
	:param lat: Широта
	:param lon: Довгота
	:return: dict weather data
	"""
	url = 'https://api.openweathermap.org/data/2.5/weather'
	l = ['ua', 'ru', 'en']
	shuffle(weather_api_key)
	for i, e in enumerate(news_api_key):
		async with aiohttp.request('GET', url, params={
			"appid": weather_api_key[i],
			"lat": lat,
			"lon": lon,
			"units": "metric",
			"lang": l[ln]
		}) as response:
			if response.status == 200 and await response.text():
				data = await response.text()
				return json.loads(data)


async def weather(lat, lon, ln=1) -> str:
	"""
	Отримуємо опрацьовані данні про погоду
	:param lat: Довгота
	:param lon: Широта
	:param ln: Мова
	:return: готова стрічка з даними
	"""
	data = await weather_request(lat, lon, ln)
	if data['cod'] == 200:
		result = dict(
			name=data['name'],
			country=data['sys']['country'],
			sunrise=data['sys']['sunrise'],
			sunset=data['sys']['sunset'],
			timezone=data['timezone'],
			temp=round(data['main']['temp']),
			feels_like_temp=round(data['main']['feels_like']),
			pressure=data['main']['pressure'],
			humidity=data['main']['humidity'],
			description=data['weather'][0]['description'],
			icon=data['weather'][0]['icon'],
		)
		return result


async def weather_detail_request(city, ln) -> dict:
	"""
	Функція запиту до OpenWeatherMap API
	:param city: Місто
	:return: dict weather data
	"""
	url = 'https://api.openweathermap.org/data/2.5/forecast'
	l = ['ua', 'ru', 'en']
	shuffle(weather_api_key)
	for i, e in enumerate(news_api_key):
		async with aiohttp.request('GET', url, params={
			"appid": weather_api_key[i],
			"q": city,
			"units": "metric",
			"lang": l[ln]
		}) as response:
			if response.status == 200 and await response.text():
				data = await response.text()
				return json.loads(data)


async def weather_detail(city, ln=1) -> str:
	"""
	Отримуємо опрацьовані данні про погоду
	:param city: Назва міста
	:param ln: Мова
	:return: готова стрічка з даними
	"""
	data = await weather_detail_request(city, ln)
	if data['cod'] == 200:
		result = dict(
			name=data['name'],
			country=data['sys']['country'],
			sunrise=data['sys']['sunrise'],
			sunset=data['sys']['sunset'],
			timezone=data['timezone'],
			temp=round(data['main']['temp']),
			feels_like_temp=round(data['main']['feels_like']),
			pressure=data['main']['pressure'],
			humidity=data['main']['humidity'],
			description=data['weather'][0]['description'],
			icon=data['weather'][0]['icon'],
		)
		return result

async def random_news(ln) -> dict:
	"""
	Функція для отримання випадкової новини на потрібній мові
	:param ln: Мовний код
	:return: Словник з данними про новину
	"""
	data = await news_request(ln)
	if data:
		shuffle(data)
		data_array = []
		for el in data:
			title = await text_news_filter(el['title'])
			description = await text_news_filter(el['description'])
			data_array_pre = [
				title,
				description,
				el['source']['name'],
				el['url'],
				el['urlToImage'],
			]
			data_array.append(data_array_pre)
		return data_array


async def get_news(array, id_el, id_user) -> dict:
	"""
	Видача елемента за ідентифікатором елемента та користувача
	:param array: Загальний масив
	:param id_el: Ідентифікатор елемента
	:param id_user: Ідентифікатор користувача
	:return:
	"""
	for i in array:
		if i[0] == id_user:
			try:
				return i[1][id_el]
			except Exception as e:
				logging.error(e)
				return False


async def message_news_prepare(title, text, source_name, url, ln) -> str:
	"""
	Підготовка повідомлення з новиною
	:param title: Заголовок
	:param text: Текст
	:param source_name: Назва джерела
	:param url: Посилання на джерело
	:param ln: Мова
	:return: Строка готового повідомлення
	"""
	return msg.news_template[ln] % (title, text, url, source_name)


async def text_news_filter(string) -> str:
	"""
	Функція для підготовки тексту новини
	:param string: Вхідна строка
	:return: Оброблена строка
	"""
	string = str(string).replace('https://', '').replace('http://', '')
	result = string.replace('&raquo;', '').replace('&laquo;', '').replace('&nbsp;', '')
	x = await cleanhtml(result)
	return x


async def check_news_search(string) -> bool:
	s = "".join(x for x in string if x.isalpha() or x.isspace())
	return [True for i in s.lower().split() if i in news_check_words]