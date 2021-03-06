import config, logging, os, re
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
	get_news, message_news_prepare, weather, check_limit,
	rand_hex_string, qwriter_create_page
)

from qiwi_api import create_payment_url as create_payment_qiwi
from qiwi_api import get_amount_pay, verify_payment

from weather_image import generator_weather_image

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

db_path = os.path.abspath("%s/db.db" % config.bot_root)
db = SQLight(db_path)

news_array = []
last_news_msg_get = []

class AdminStates(StatesGroup):
	contact_admin = State()
	admin_ad_menu = State()
	buy_bonus = State()


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
				[['Unban user ???', f'unban1_action:{user_id}']]
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


@dp.callback_query_handler(lambda call_back: 'recheck_pay:' in call_back.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
	ln = db.subscriber_get_lang(callback_query.from_user.id)
	try:
		await dp.throttle('recheck_pay', rate=1.5)
	except Throttled:
		try:
			await dp.throttle('recheck_pay_', rate=1)
		except Throttled:
			pass
		else:
			await bot.answer_callback_query(
				callback_query.id,
				text=msg.slowly_pleas[ln],
			)
	else:
		token = str(callback_query.data).replace('recheck_pay:', '')
		await check_payment_local(token, callback_query)
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
			lc_menu = await menu(callback_query)
			try:
				iv_link = await qwriter_create_page(el[0])
				await bot.send_message(
					chat_id=callback_query.from_user.id,
					text=msg.search_data_send_template[ln] % (
						iv_link, el[0], el[1], el[2], f'@{me.username}'
					),
					disable_web_page_preview=False,
					reply_markup=lc_menu,
				)
			except Exception as e:
				logging.error(e)
				await bot.send_message(
					chat_id=callback_query.from_user.id,
					text=msg.search_data_send_template_no_iv[ln] % (
						el[0], el[1], el[2], f'@{me.username}'
					),
					disable_web_page_preview=True,
					reply_markup=lc_menu,
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

	async def local_news_id_update(user_id, msg_) -> None:
		global last_news_msg_get
		msg_ = msg_.message_id
		add = False
		for i in last_news_msg_get:
			if i[0] == user_id:
				i[1] = msg_
				add = True
		if not add:
			last_news_msg_get.append(
				[
					user_id,
					msg_,
				]
			)

	async def get_last_news_id(user_id) -> int:
		global last_news_msg_get
		for i in last_news_msg_get:
			if i[0] == user_id:
				return i[1]

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
				for x, i in enumerate(news_array):
					if i[0] == callback_query.from_user.id:
						news_array.pop(x)
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
						n_msg = await bot.send_photo(
							callback_query.from_user.id,
							feed[4],
							nw_str,
							reply_markup=nw_buttons,
						)
					except Exception as e:
						logging.error(e)
						n_msg = await bot.send_photo(
							callback_query.from_user.id,
							open(config.news_default_background, 'rb'),
							nw_str,
							reply_markup=nw_buttons,
						)
				else:
					n_msg = await bot.send_photo(
						callback_query.from_user.id,
						open(config.news_default_background, 'rb'),
						nw_str,
						reply_markup=nw_buttons,
					)
				await local_news_id_update(callback_query.from_user.id, n_msg)
			else:
				await bot.send_message(
					callback_query.from_user.id,
					msg.news_error_get[ln],
				)
	elif token != 9999:
		try:
			await dp.throttle('news_get', rate=1)
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
					nw_buttons = await create_inline_buttons(
						[[msg.news_view_finish_button[ln], 'aware_news:9999']]
					)
					await send_admins_msg(
						'Actions',
						callback_query.from_user.username,
						callback_query.from_user.full_name,
						callback_query.from_user.id,
						'Looked at everything news',
					)
				d_news = await get_last_news_id(callback_query.from_user.id)
				try:
					await bot.delete_message(
						callback_query.from_user.id,
						d_news,
					)
				except Exception as e:
					logging.error(e)
				if feed[4]:
					try:
						n_msg = await bot.send_photo(
							callback_query.from_user.id,
							feed[4],
							nw_str,
							reply_markup=nw_buttons,
						)
					except Exception as e:
						logging.error(e)
						n_msg = await bot.send_photo(
							callback_query.from_user.id,
							open(config.news_default_background, 'rb'),
							nw_str,
							reply_markup=nw_buttons,
						)
				else:
					n_msg = await bot.send_photo(
						callback_query.from_user.id,
						open(config.news_default_background, 'rb'),
						nw_str,
						reply_markup=nw_buttons,
					)
				await local_news_id_update(callback_query.from_user.id, n_msg)
			else:
				await bot.send_message(
					callback_query.from_user.id,
					msg.no_news_more[ln],
				)
	else:
		d_news = await get_last_news_id(callback_query.from_user.id)
		try:
			await bot.delete_message(
				callback_query.from_user.id,
				d_news,
			)
		except Exception as e:
			logging.error(e)
		try:
			await bot.send_photo(
				callback_query.from_user.id,
				open(config.news_finish_background, 'rb'),
				msg.news_view_finish_notify[ln],
			)
		except Exception as e:
			await bot.send_message(
				callback_query.from_user.id,
				msg.news_view_finish_notify[ln],
			)
			logging.error(e)
	if no_answer:
		await bot.answer_callback_query(callback_query.id)


async def get_button_name(data, buttons) -> str:
	"""
	?????????????? ?????? ?????????????????? ?? ???????????????? ?????????? ????????????
	:param data: ???????????? ?????? ??????????????
	:param buttons: ?????????? ?? ????????????????
	:return: ?????????? ????????????
	"""
	for i, e in enumerate(buttons["inline_keyboard"]):
		x = e[0]['callback_data']
		if x == data:
			return buttons["inline_keyboard"][i][0]['text']


async def lang_select(message) -> None:
	"""
	?????????????? ???????????? ????????
	:param message: ???????? ???????????????????????? (??????????????)
	:return: None
	"""
	buttons = await create_inline_buttons([['????????', 'select_lang:0'], ['????????', 'select_lang:1'], ['????????', 'select_lang:2']])
	await bot.send_message(
		message.from_user.id,
		'???????? ?????????????? ????????\n???????? ???????????????? ????????\n???????? Select language',
		reply_markup=buttons
	)


async def limit_info(message) -> None:
	"""
	?????????????????????? ?????? ?????????????? /limit
	:param message: ???????? ???????????????????? ???????????????????????? ?????? ??????????????????????
	:return: None
	"""
	u = message.from_user.id
	ln = db.subscriber_get_lang(u)
	d = db.subscriber_get_from_user_id(u)[0]
	prem = d[9]
	limit = d[8]
	default_max = config.default_limit
	exc = (default_max + prem) - limit
	await bot.send_message(
		u, msg.limit_menu_msg[ln] % (prem, limit, exc)
	)


async def menu(message) -> dict:
	"""
	??????????????, ???? ???????????????? ?????????????????????????????? ????????
	:param message: ???????? ????????????????????????
	:return: ????????
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
	?????????????? ?????? ?????????????????? ???????????? "??????????????????" ???????????????????? ?????????????? ????????
	:param message: ???????? ????????????????????????
	:return: dict
	"""
	c = cancel
	ln = db.subscriber_get_lang(message.from_user.id)
	c['keyboard'][0][0]['text'] = msg.cancel_btns[ln]
	return c


async def check_payment_local(token, message) -> None:
	"""
	???????????????? ?????????????????? ??????????????
	:param token: ??????????
	:param message: ???????? ????????????????????????
	:return: None
	"""
	u = message.from_user.id
	try:
		msg_ = message.id
		inline = True
	except Exception as e:
		inline = False
		logging.error(e)
	ln = db.subscriber_get_lang(u)
	data = await verify_payment(token, db)
	if data:
		but = msg.pay_check_repeat[ln]
		button = await create_inline_buttons(
			[[but, 'recheck_pay:%s' % token]]
		)
		if data == '??????????!':
			try:
				payment = db.search_payment_by_token(token)[0]
				bonus = payment[7]
				status = payment[6]
				if not status:
					db.update_custom_field(u, 'premium', bonus, 1)
					db.update_custom_field_payments(token, 'status', 1) # ???????????????????? ???? ??????????????????
					d = await rand_hex_string()
					if inline:
						await bot.answer_callback_query(message.id, msg.pay_success[ln])
					else:
						await bot.send_message(u, msg.pay_success[ln] + '\n\n<code>%s</code>' % d)
				else:
					if inline:
						await bot.answer_callback_query(message.id, msg.already_been_paid[ln])
					else:
						await bot.send_message(u, msg.already_been_paid[ln], reply_markup=button)
			except Exception as e:
				logging.error(e)
				if inline:
					await bot.answer_callback_query(message.id, msg.unknown_pay_error[ln])
				else:
					await bot.send_message(u, msg.unknown_pay_error[ln], reply_markup=button)
		else:
			if inline:
				await bot.answer_callback_query(message.id, msg.pay_error[ln] % data, True)
			else:
				await bot.send_message(u, msg.pay_error[ln] % data, reply_markup=button)
	else:
		await bot.send_message(u, msg.unknown_pay_error[ln])


@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
	if '/start ' in message.text:
		token = message.text.replace('/start ', '')
		await check_payment_local(token, message)
	else:
		if not db.subscriber_exists(message.from_user.id):
			db.add_subscriber(message.from_user.id, message.from_user.full_name)
			logging.info("Save user [ID: %s] [FULL_NAME: %s]" % (message.from_user.id, message.from_user.full_name))
			await lang_select(message)
		else:
			await message.answer(msg.start_message[db.subscriber_get_lang(message.from_user.id)], reply_markup=await menu(message))


@dp.message_handler(commands=['lang'])
async def lang(message: types.Message):
	await lang_select(message)


@dp.message_handler(commands=['limit'])
async def lang(message: types.Message):
	await limit_info(message)


@dp.message_handler(commands=['bonus'])
async def lang(message: types.Message):
	ln = db.subscriber_get_lang(message.from_user.id)
	await message.reply(msg.payment_create[ln], reply_markup=await cancel_menu(message))
	await AdminStates.buy_bonus.set()


@dp.message_handler(state=AdminStates.buy_bonus)
async def state_check_func_ntf(message: types.Message, state: FSMContext):
	cancel = False
	ln = db.subscriber_get_lang(message.from_user.id)
	if message.text == msg.cancel_btns[ln]:
		await message.reply(msg.cancel_msg[ln],  reply_markup=await menu(message))
		cancel = True

	if not cancel:
		if len(message.text) < 8:
			num = int(''.join(filter(str.isdigit, message.text)))
			if num:
				if num > 5 and num <= 1000:
					a = await get_amount_pay(num)
					amount = a['rub_price']
					b = await bot.get_me()
					pseudo = b.username
					p_data = await create_payment_qiwi(
						amount, pseudo, db, message, num
					)
					url = p_data['url']
					buttons = await create_inline_buttons(
						[[msg.pay_button[ln], url]], url=True
					)
					await message.reply(
						msg.payment_check[ln] % (amount, num),
						reply_markup=buttons
					)
					await message.reply(
						msg.menu_update_notify[ln],
						reply_markup=await menu(message)
					)
				else:
					await message.reply(msg.payment_sum_error[ln], reply_markup=await menu(message))
			else:
				await message.reply(msg.payment_num_error[ln], reply_markup=await menu(message))
		else:
			await message.reply(msg.long_msg[ln], reply_markup=await menu(message))

	return await state.finish()



@dp.message_handler(commands=['help', 'h'])
async def lang(message: types.Message):
	ln = db.subscriber_get_lang(message.from_user.id)
	await message.answer(msg.help_menu_msg[ln])


async def send_admins_msg(type, pseudo, fullname, user_id, text, reply_mk=None) -> None:
	"""
	??????????????, ???? ???????????????? ???????????????????????? ??????????????????????????????
	:param type: ?????? ????????????????????????
	:param pseudo: ?????????????????? ??????????????????????
	:param fullname: ?????????? ????'?? ??????????????????????
	:param user_id: ?????????????????????????? ??????????????????????
	:param text: ?????????? ????????????????????????
	:return: None
	"""
	if not pseudo:
		pseudo = 'No found username'
	else:
		pseudo = f'@{pseudo}'
	if type == 'Support':
		db.add_contact_ticket(pseudo, fullname, user_id, text)
	if str(user_id) not in config.admins and not reply_mk:
		buttons = await create_inline_buttons(
			[['Ban user ????', 'ban_action:%s' % user_id]]
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
		await message.reply('???? ?????????????? ???? ?? ????????????????. ?????????? - "%s"' % message.text,  reply_markup=await menu(message))

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
				cl = await check_limit(message, db)
				if cl:
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
						await message.reply(msg.unknown_error[ln], reply_markup=await menu(message))
				else:
					await message.reply(msg.limit_search_msg[ln], reply_markup=await menu(message))
			else:
				await message.reply(msg.long_msg[ln],  reply_markup=await menu(message))


@dp.message_handler(content_types=['location'])
async def handle_message_received_location(message):
	# ln = db.subscriber_get_lang(message.from_user.id)
	# w = await weather(message.location.latitude, message.location.longitude, ln)
	# x = await generator_weather_image(w, ln)
	# await message.reply_photo(open(x, 'rb'))
	# from os import remove
	# remove(x)
	await message.reply('We are sorry, but this feature is still under development.')


async def shutdown(dispatcher: Dispatcher):
	await dispatcher.storage.close()
	await dispatcher.storage.wait_closed()


if __name__ == '__main__':
	executor.start_polling(dp, loop=loop, skip_updates=False, on_shutdown=shutdown)