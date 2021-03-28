from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton('Зворотній зв\'язок'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(KeyboardButton('Скасувати'))


async def create_inline_buttons(buttons, load_more_button=False, limit=0, url=False) -> dict:
    """Функция генерации Inline кнопок"""

    array_button = []
    global_array_buttons = []
    type_ = "callback_data"
    if url:
        type_ = "url"

    def add_item(x, y):
        array_button = []
        temp = {"text": f"{x}", f"{type_}": f"{y}"}
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
        temp = {"text": "🔽", "callback_data": "load_more"}
        array_button.append(temp)
        global_array_buttons.append(array_button)

    result = dict(inline_keyboard=global_array_buttons)

    return result


async def append_button_to_inline_dict_buttons(dict_buttons, button) -> dict:
    """
    Функція яка додає кнопку до словник вже існуючих кнопок
    :param dict_buttons: Словник з кнопками
    :param button: Кнопка обгорнута в список
    :return: Модифікований словник
    """
    x = dict_buttons
    x = x['inline_keyboard'] + [[{'text': button[0], 'callback_data': button[1]}]]
    return dict(inline_keyboard=x)


async def append_button_to_keyboard_dict_buttons(dict_buttons, button) -> dict:
    """
    Функція яка додає кнопку до словник вже існуючих кнопок (клавіатура)
    :param dict_buttons: Словник з кнопками
    :param button: Кнопка обгорнута в список
    :return: Модифікований словник
    """
    x = dict_buttons
    x = x['keyboard'] + [[{'text': button}]]
    if dict_buttons['resize_keyboard']:
        return dict(keyboard=x, resize_keyboard=True)
    else:
        return dict(keyboard=x)