from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton('Зворотній зв\'язок'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(KeyboardButton('Скасувати'))

async def create_inline_buttons(buttons, load_more_button=False, limit=0):
    """Функция генерации Inline кнопок"""

    array_button = []
    global_array_buttons = []

    def add_item(x, y):
        array_button = []
        temp = {"text": f"{x}", "callback_data": f"{y}"}
        array_button.append(temp)
        global_array_buttons.append(array_button)

    if limit and len(buttons) <= limit:
        load_more_button = False

    for x, i in enumerate(buttons):
        if limit and x < limit:
            add_item(i[0], i[1])
        elif not limit:
            add_item(i[0], i[1])

    if load_more_button:
        array_button = []
        temp = {"text": "Ещё", "callback_data": "load_more"}
        array_button.append(temp)
        global_array_buttons.append(array_button)

    result = dict(inline_keyboard=global_array_buttons)

    return result