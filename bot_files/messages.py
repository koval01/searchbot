# subscribe_ok = "Вы успешно подписались на рассылку!\nЕсли вы не хотите, чтобы бот присылал Вам уведомление, то Вы можете в \
# любой момент отменить подписку. (/unsubscribe)"
# subscribe_fail = 'Вы уже подписаны.'
# unsubscribe_ok = 'Вы успешно отписались от уведомлений.'
# unsubscribe_fail = 'Вы и не были подписаны.'
# search_start = 'Введите название команды, или фрагмент начала её названия.'
# error_send = 'Произошла ошибка - %s'
# menu_updated =  'Меню обновленно...'
# cancel_msg = 'Хорошо, Вы покинули это меню.'
# find_team_num = 'По запросу - "%s" было найдено %s вариантов. Показано %s из %s элементов. (%s сек.)'
# rate_limit_button = 'Кликай медлнее'
# button_inline_notify = 'Обработка данных...'
# button_inline_notify_two = 'Данные о команде отправлены'


menu_update_notify = 'Оновлюю меню...'
slowly_pleas = 'Будь ласка зачекай перед наступним запитом'
unknown_error = 'Я не зміг нічого знайти за твоїм запитом, пробач.'
button_inline_notify = 'Надсилаю - "%s"'
start_message = 'Привіт, що ти хочеш знайти?'
cancel_msg = 'Гаразд, ви покинули це меню.'
long_msg = 'Ваше повідомлення занадто довге.'
short_msg = 'В повідомленні має бути, щонайменше 30 символів'
message_sent = 'Повідомлення успішно надіслано адміністраторам.'
error_sentences = 'Повідомлення не пройшло перевірку. Переконайтеся, що воно є коректним.'
admin_ad_help = 'Надішли мені будь ласка рекламний текст (максимальна довжина повідомлення в Telegram - 4096 символів). Щоб вийти з цього мені нажми "Скасувати" нижче.'
contact_help = 'Опишіть своє питання чи побажання. Якщо у вас не встановлений псевдонім в профілі Telegram, то напишіть як з вами можна зв\'язатися. Довжина повідомлення може бути від 30 до 1000 символів. У разі якщо ви потрапили в це меню випадково, натисніть нижче "Скасувати".'
button_inline_error = 'Не вдалося отримати дані, можливо вони застаріли'
ban_message = 'Схоже адміністрація обмежила вам доступ через порушення правил чи дуже активний темп користування (флуд).'
search_done_msg = 'За запитом "<b>%s</b>" було знайдено приблизно <b>%s</b> результатів. З них показані <b>%s</b> найбільш релевантних. (<b>%s</b> сек.)'

search_data_send_template = """
<a href="%s"><b>%s</b></a>

%s

%s
"""

async def check_user_msg(string) -> str:
    """
    Перевірка тексту користувача
    :param string: Строка яку потрібно перевірити
    :return: Результат
    """
    if len(string) > 1000:
        return long_msg
    elif len(string) < 29:
        return short_msg
    elif len(string.split()) < 10:
        return error_sentences
    else:
        for i in string.split():
            if len(i) > 24:
                return error_sentences