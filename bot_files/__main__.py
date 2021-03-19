import config, logging, os
from asyncio import get_event_loop

import messages as msg
from messages import check_user_msg

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from api_module import (
	data_get, data_prepare, cleanhtml, search_and_decode_el,
	title_cut, check_admin, random_news, check_news_search,
	get_news, message_news_prepare
)

from sqlcontroller import SQLight

from buttons import (
	create_inline_buttons, cancel,
	append_button_to_keyboard_dict_buttons, append_button_to_inline_dict_buttons
)
from buttons import menu as menu_original


logging.basicConfig(format=config.format_logging, level=logging.INFO)

loop = get_event_loop()
bot = Bot(token=config.API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()

dp = Dispatcher(bot, loop=loop, storage=storage)
dp.middleware.setup(LoggingMiddleware())

db_path = os.path.abspath("db.db")
db = SQLight(db_path)

news_array = []

class AdminStates(StatesGroup):
	contact_admin = State()
	admin_ad_menu = State()


@dp.callback_query_handler(lambda call_back: 'select_lang:' in call_back.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
	ln = int(callback_query.data.replace('select_lang:', ''))
	db.update_lang(
		callback_query.from_user.id, ln
	)
	await bot.send_message(
		callback_query.from_user.id,
		msg.start_message[ln],
			reply_markup=await menu(callback_query)
	)
	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda call_back: 'ban_action:' in call_back.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
	a_result = await check_admin(callback_query)
	if a_result:
		user_id = callback_query.data.replace('ban_action:', '')
		ln = db.subscriber_get_lang(callback_query.from_user.id)
		data = db.subscriber_get_from_user_id(user_id)[0]
		if not data[5]:
			db.update_ban(user_id)
			buttons = await create_inline_buttons(
				[['Unban user ✅', f'unban1_action:{user_id}']]
			)
			await bot.send_message(
				callback_query.from_user.id,
				'You blocked %s (%s)' % (data[3], user_id),
				reply_markup=buttons
			)
			await send_admins_msg(
				'Ban',
				callback_query.from_user.username,
				callback_query.from_user.full_name,
				callback_query.from_user.id,
				'Ban user %s (%s)' % (data[3], user_id),
				buttons,
			)
		else:
			await bot.send_message(
				callback_query.from_user.id,
				msg.already_banned[ln]
			)
	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda call_back: 'unban1_action:' in call_back.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
	a_result = await check_admin(callback_query)
	if a_result:
		user_id = callback_query.data.replace('unban1_action:', '')
		ln = db.subscriber_get_lang(callback_query.from_user.id)
		data = db.subscriber_get_from_user_id(user_id)[0]
		if data[5]:
			db.update_ban(user_id, 0)
			await bot.send_message(
				callback_query.from_user.id,
				'You unblocked %s (%s)' % (data[3], user_id),
			)
			await send_admins_msg(
				'Ban',
				callback_query.from_user.username,
				callback_query.from_user.full_name,
				callback_query.from_user.id,
				'Unban user %s (%s)' % (data[3], user_id),
			)
		else:
			await bot.send_message(
				callback_query.from_user.id,
				msg.already_unbanned[ln]
			)
	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda call_back: 'inline_data:' in call_back.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
	ln = db.subscriber_get_lang(callback_query.from_user.id)
	try:
		await dp.throttle('text', rate=1)
	except Throttled:
		try:
			await dp.throttle('text_', rate=0.6)
		except Throttled:
			pass
		else:
			await bot.answer_callback_query(
				callback_query.id,
				text=msg.slowly_pleas[ln],
			)
	else:
		token = str(callback_query.data).replace('inline_data:', '')
		await bot.send_chat_action(callback_query.from_user.id, 'typing')
		el = await search_and_decode_el(token)
		if el:
			me = await bot.get_me()
			await bot.send_message(
				chat_id=callback_query.from_user.id,
				text=msg.search_data_send_template[ln] % (
					el[0], el[1], el[2], f'@{me.username}'
				),
				disable_web_page_preview=True,
				reply_markup=await menu(callback_query),
			)

			d = callback_query.data
			buttons = callback_query.message.reply_markup
			button_name = await get_button_name(d, buttons)
			message = callback_query

			await send_admins_msg(
				'Select',
				message.from_user.username,
				message.from_user.full_name,
				message.from_user.id,
				button_name,
			)

			await bot.answer_callback_query(
				callback_query.id,
				text=msg.button_inline_notify[ln] % button_name,
			)
		else:
			await bot.answer_callback_query(
				callback_query.id,
				text=msg.button_inline_error[ln],
			)


@dp.callback_query_handler(lambda call_back: 'aware_news:' in call_back.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
	token = int(callback_query.data.replace('aware_news:', ''))
	ln = db.subscriber_get_lang(callback_query.from_user.id)
	no_answer = True
	if token == 0:
		try:
			await dp.throttle('news', rate=7200)
		except Throttled:
			await bot.send_message(
				callback_query.from_user.id,
				msg.news_no[ln],
			)
		else:
			await send_admins_msg(
				'Select',
				callback_query.from_user.username,
				callback_query.from_user.full_name,
				callback_query.from_user.id,
				msg.news_button[ln],
			)
			news_data = await random_news(ln)
			if news_data:
				global news_array
				news_array.append(
					[
						callback_query.from_user.id,
						news_data,
					]
				)
				feed = await get_news(
					news_array, token,
					callback_query.from_user.id
				)
				nw_str = await message_news_prepare(
					feed[0], feed[1], feed[2], feed[3], ln
				)
				nw_buttons = await create_inline_buttons(
					[[msg.news_scroll[ln], 'aware_news:1']]
				)
				if feed[4]:
					try:
						await bot.send_photo(
							callback_query.from_user.id,
							feed[4],
							nw_str,
							reply_markup=nw_buttons,
						)
					except Exception as e:
						logging.error(e)
						await bot.send_message(
							callback_query.from_user.id,
							nw_str,
							reply_markup=nw_buttons,
							disable_web_page_preview=True,
						)
				else:
					await bot.send_message(
						callback_query.from_user.id,
						nw_str,
						reply_markup=nw_buttons,
						disable_web_page_preview=True,
					)
			else:
				await bot.send_message(
					callback_query.from_user.id,
					msg.news_error_get[ln],
				)
	else:
		try:
			await dp.throttle('news_get', rate=1.5)
		except Throttled:
			await bot.answer_callback_query(
				callback_query.id,
				msg.news_slowly[ln],
			)
			no_answer = False
		else:
			feed = await get_news(
				news_array, token,
				callback_query.from_user.id
			)
			if feed:
				test_feed = await get_news(
					news_array, token + 1,
					callback_query.from_user.id
				)
				nw_str = await message_news_prepare(
					feed[0], feed[1], feed[2], feed[3], ln
				)
				if test_feed:
					nw_buttons = await create_inline_buttons(
						[[msg.news_scroll[ln], 'aware_news:%s' % str(token + 1)]]
					)
				else:
					nw_buttons = None
					await send_admins_msg(
						'Actions',
						callback_query.from_user.username,
						callback_query.from_user.full_name,
						callback_query.from_user.id,
						'Looked at everything news',
					)
				if feed[4]:
					try:
						await bot.send_photo(
							callback_query.from_user.id,
							feed[4],
							nw_str,
							reply_markup=nw_buttons,
						)
					except Exception as e:
						logging.error(e)
						await bot.send_message(
							callback_query.from_user.id,
							nw_str,
							reply_markup=nw_buttons,
							disable_web_page_preview=True,
						)
				else:
					await bot.send_message(
						callback_query.from_user.id,
						nw_str,
						reply_markup=nw_buttons,
						disable_web_page_preview=True,
					)
			else:
				await bot.send_message(
					callback_query.from_user.id,
					msg.no_news_more[ln],
				)
	if no_answer:
		await bot.answer_callback_query(callback_query.id)


async def get_button_name(data, buttons) -> str:
	"""
	Функція для отримання з каллбеку назви кнопки
	:param data: Кнопка яку шукаємо
	:param buttons: Масив з кнопками
	:return: Назва кнопки
	"""
	for i, e in enumerate(buttons["inline_keyboard"]):
		x = e[0]['callback_data']
		if x == data:
			return buttons["inline_keyboard"][i][0]['text']


async def lang_select(message) -> None:
	"""
	Функція вибору мови
	:param message: Тіло повідомлення (команди)
	:return: None
	"""
	buttons = await create_inline_buttons([['🇺🇦', 'select_lang:0'], ['🇷🇺', 'select_lang:1'], ['🇺🇸', 'select_lang:2']])
	await bot.send_message(
		message.from_user.id,
		'🇺🇦 Оберіть мову\n🇷🇺 Выберите язык\n🇺🇸 Select language',
		reply_markup=buttons
	)


async def menu(message) -> dict:
	"""
	Функція, що повертає персоналізоване меню
	:param message: Тіло повідомлення
	:return: Меню
	"""
	ln = db.subscriber_get_lang(message.from_user.id)

	a_result = await check_admin(message)
	edited_menu = menu_original
	edited_menu['keyboard'][0][0]['text'] = msg.support_btns[ln]
	if a_result:
		edited_menu = await append_button_to_keyboard_dict_buttons(
			edited_menu, msg.menu_btns[ln][1]
		)
	return edited_menu


async def cancel_menu(message) -> dict:
	"""
	Функція для стоврення кнопки "скасувати" відповідно обраної мови
	:param message: Тіло повідомлення
	:return: dict
	"""
	c = cancel
	ln = db.subscriber_get_lang(message.from_user.id)
	c['keyboard'][0][0]['text'] = msg.cancel_btns[ln]
	return c


@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
	if not db.subscriber_exists(message.from_user.id):
		db.add_subscriber(message.from_user.id, message.from_user.full_name)
		logging.info("Save user [ID: %s] [FULL_NAME: %s]" % (message.from_user.id, message.from_user.full_name))
		await lang_select(message)
	else:
		await message.answer(msg.start_message[db.subscriber_get_lang(message.from_user.id)], reply_markup=await menu(message))


@dp.message_handler(commands=['lang'])
async def lang(message: types.Message):
	await lang_select(message)


async def send_admins_msg(type, pseudo, fullname, user_id, text, reply_mk=None) -> None:
	"""
	Функція, що надсилає повідомлення адміністраторам
	:param type: Тип повідомлення
	:param pseudo: Псевдонім користувача
	:param fullname: Повне ім'я користувача
	:param user_id: Ідентифікатор користувача
	:param text: Текст повідомлення
	:return: None
	"""
	if not pseudo:
		pseudo = 'No found username'
	else:
		pseudo = f'@{pseudo}'
	if type == 'Support':
		db.add_contact_ticket(pseudo, fullname, user_id, text)
	if user_id not in config.admins and not reply_mk:
		buttons = await create_inline_buttons(
			[['Ban user 🚫', 'ban_action:%s' % user_id]]
		)
	elif reply_mk:
		buttons = reply_mk
	else:
		buttons = None
	for i in config.admins:
		if int(i) != int(user_id):
			try:
				await bot.send_message(
					chat_id=i,
					text='[%s] %s (%s) "%s"' % (type, fullname, pseudo, text),
					reply_markup=buttons,
				)
			except Exception as e:
				logging.error(e)


@dp.message_handler(state=AdminStates.contact_admin)
async def state_check_func_ntf(message: types.Message, state: FSMContext):
	cancel = False
	ln = db.subscriber_get_lang(message.from_user.id)
	if message.text == msg.cancel_btns[ln]:
		await message.reply(msg.cancel_msg[ln],  reply_markup=await menu(message))
		cancel = True

	if not cancel:
		if len(message.text) < 1001:
			sentence_check = await check_user_msg(message.text, ln)
			if sentence_check:
				await message.reply(sentence_check,  reply_markup=await menu(message))
			else:
				await send_admins_msg(
					'Contact',
					message.from_user.username,
					message.from_user.full_name,
					message.from_user.id,
					message.text,
				)
				await message.reply(msg.message_sent[ln],  reply_markup=await menu(message))
		else:
			await message.reply(msg.long_msg[ln],  reply_markup=await menu(message))

	return await state.finish()


@dp.message_handler(state=AdminStates.admin_ad_menu)
async def state_check_func_ntf(message: types.Message, state: FSMContext):
	cancel = False
	ln = db.subscriber_get_lang(message.from_user.id)
	if message.text == msg.cancel_btns[ln]:
		await message.reply(msg.cancel_msg[ln],  reply_markup=await menu(message))
		cancel = True

	if not cancel:
		await message.reply('Ця функція ще в розробці. Текст - "%s"' % message.text,  reply_markup=await menu(message))

	return await state.finish()


@dp.message_handler(content_types=['text'])
async def handle_message_received_text(message):
	ln = db.subscriber_get_lang(message.from_user.id)
	try:
		await dp.throttle('text', rate=1)
	except Throttled:
		try:
			await dp.throttle('text_', rate=0.6)
		except Throttled:
			pass
		else:
			await message.reply(msg.slowly_pleas[ln],  reply_markup=await menu(message))
	else:
		if db.subscriber_get_from_user_id(message.from_user.id)[0][5]:
			await message.reply(msg.ban_message[ln],  reply_markup=await menu(message))
		else:
			a_result = await check_admin(message)
			if message.text == msg.menu_btns[ln][0]:
				await message.reply(msg.contact_help[ln], reply_markup=await cancel_menu(message))
				await AdminStates.contact_admin.set()
			elif message.text == msg.menu_btns[ln][1] and a_result:
				await message.reply(msg.admin_ad_help[ln], reply_markup=await cancel_menu(message))
				await AdminStates.admin_ad_menu.set()
			elif not message.is_command() and len(message.text) < 2000:
				await bot.send_chat_action(message.from_user.id, 'typing')
				text = message.text.replace('@', '').replace('#', '')
				x = await data_get(text)
				x = await data_prepare(x)
				if x:
					template_items = x[0]
					title = await cleanhtml(message.text)
					title = await title_cut(title)
					nw = await check_news_search(message.text)
					if nw:
						nw_button = msg.news_button[ln]
						buttons = await create_inline_buttons(
							[[nw_button, 'aware_news:0']]
						)
						for i in x[1:]:
							buttons = await append_button_to_inline_dict_buttons(
								buttons, i
							)
					else:
						buttons = await create_inline_buttons(x[1:])
					await message.reply(msg.search_done_msg[ln] % (
						title,
						template_items['TotalResults'],
						len(x) - 1,
						template_items['SearchTime'],
					), reply_markup=buttons)
					await send_admins_msg(
						'Search',
						message.from_user.username,
						message.from_user.full_name,
						message.from_user.id,
						title,
					)
				else:
					await message.reply(msg.unknown_error[ln],  reply_markup=await menu(message))
			else:
				await message.reply(msg.long_msg[ln],  reply_markup=await menu(message))


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False)