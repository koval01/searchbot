import aiohttp, logging, json, string, re
from random import choice, randint, shuffle
from config import api_host_search, api_key, cx, admins


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