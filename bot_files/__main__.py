import config, logging, re, os
from asyncio import get_event_loop
import messages as msg
from messages import check_user_msg

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from api_module import data_get, data_prepare, cleanhtml, search_and_decode_el, title_cut
from sqlcontroller import SQLight
from buttons import create_inline_buttons, menu, cancel


logging.basicConfig(format=config.format_logging, level=logging.INFO)

loop = get_event_loop()
bot = Bot(token=config.API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()

dp = Dispatcher(bot, loop=loop, storage=storage)
dp.middleware.setup(LoggingMiddleware())

db_path = os.path.abspath("db.db")
db = SQLight(db_path)

class AdminStates(StatesGroup):
	contact_admin = State()


@dp.callback_query_handler(lambda call_back: call_back.data == re.search(r"inline_data:\S*", call_back.data)[0])
async def process_callback_button1(callback_query: types.CallbackQuery):
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
				text=msg.slowly_pleas,
			)
	else:
		token = str(callback_query.data).replace('inline_data:', '')
		await bot.send_chat_action(callback_query.from_user.id, 'typing')
		el = await search_and_decode_el(token)
		if el:
			await bot.send_message(
				chat_id=callback_query.from_user.id,
				text=msg.search_data_send_template % (
					el[0], el[1], el[2]
				),
				disable_web_page_preview=True,
				reply_markup=menu,
			)

			d = callback_query.data
			buttons = callback_query.message.reply_markup
			button_name = await get_button_name(d, buttons)
			message = callback_query

			await send_admins_msg(
				'Вибір',
				message.from_user.username,
				message.from_user.full_name,
				message.from_user.id,
				button_name,
			)

			await bot.answer_callback_query(
				callback_query.id,
				text=msg.button_inline_notify,
			)
		else:
			await bot.answer_callback_query(
				callback_query.id,
				text=msg.button_inline_error,
			)


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


@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
	if not db.subscriber_exists(message.from_user.id):
		db.add_subscriber(message.from_user.id, message.from_user.full_name)
		logging.info("Save user [ID: %s] [FULL_NAME: %s]" % (message.from_user.id, message.from_user.full_name))
	await message.answer(msg.start_message, reply_markup=menu)


async def send_admins_msg(type, pseudo, fullname, user_id, text) -> None:
	"""
	Функція, що надсилає повідомлення адміністраторам
	:param type: Тип повідомлення
	:param pseudo: Псевдонім користувача
	:param fullname: Повне ім'я користувача
	:param user_id: Ідентифікатор користувача
	:param text: Текст повідомлення
	:return: None
	"""
	button = ''
	if not pseudo:
		pseudo = 'Немає псевдоніму'
	else:
		pseudo = f'@{pseudo}'
	if type == 'Зворотній зв\'язок':
		db.add_contact_ticket(pseudo, fullname, user_id, text)
		# request_id = db.add_contact_ticket(pseudo, fullname, user_id, text)[0][0]
		# button = await create_inline_buttons(['Не розглянуто', 'admin_ticket:%s' % request_id])
	for i in config.admins:
		if int(i) != int(user_id):
			if button:
				pass
			else:
				await bot.send_message(
					chat_id=i,
					text='[%s] %s (%s) "%s"' % (type, fullname, pseudo, text),
				)


@dp.message_handler(state=AdminStates.contact_admin)
async def state_check_func_ntf(message: types.Message, state: FSMContext):
	cancel = False

	if message.text == 'Скасувати':
		await message.reply(msg.cancel_msg, reply_markup=menu)
		cancel = True

	if not cancel:
		if len(message.text) < 1000:
			sentence_check = await check_user_msg(message.text)
			if sentence_check:
				await message.reply(sentence_check, reply_markup=menu)
			else:
				await send_admins_msg(
					'Зворотній зв\'язок',
					message.from_user.username,
					message.from_user.full_name,
					message.from_user.id,
					message.text,
				)
				await message.reply(msg.message_sent, reply_markup=menu)
		else:
			await message.reply(msg.long_msg, reply_markup=menu)

	return await state.finish()


@dp.message_handler(content_types=['text'])
async def handle_message_received_text(message):
	try:
		await dp.throttle('text', rate=1)
	except Throttled:
		try:
			await dp.throttle('text_', rate=0.6)
		except Throttled:
			pass
		else:
			await message.reply(msg.slowly_pleas, reply_markup=menu)
	else:
		if message.text == 'Зворотній зв\'язок':
			await message.reply(msg.contact_help, reply_markup=cancel)
			await AdminStates.contact_admin.set()
		elif not message.is_command() and len(message.text) < 2500:
			x = await data_get(message.text)
			x = await data_prepare(x)
			if x:
				buttons = await create_inline_buttons(x[1:])
				template_items = x[0]
				title = await cleanhtml(message.text)
				title = await title_cut(title)
				await message.reply(msg.search_done_msg % (
					title,
					template_items['TotalResults'],
					len(x) - 1,
					template_items['SearchTime'],
				), reply_markup=buttons)
				await send_admins_msg(
					'Пошук',
					message.from_user.username,
					message.from_user.full_name,
					message.from_user.id,
					title,
				)
			else:
				await message.reply(msg.unknown_error, reply_markup=menu)
		else:
			await message.reply(msg.long_msg, reply_markup=menu)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False)