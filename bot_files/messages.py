menu_update_notify = [
    'Оновлюю меню...',
    'Обновляю меню...',
    'Updating menu ...',
]
slowly_pleas = [
    'Будь ласка зачекай перед наступним запитом',
    'Подождите пожалуйста перед следующим запросом',
    'Please wait before the next request',
]
unknown_error = [
    'Я не зміг нічого знайти за твоїм запитом, пробач.',
    'Я не смог ничего найти по твоему запросу, прости.',
    'I could not find anything for your request, sorry.',
]
button_inline_notify = [
    'Надсилаю - "%s"',
    'Отправляю - "%s"',
    'I am sending - "%s"',
]
start_message = [
    'Привіт, що ти хочеш знайти?',
    'Привет, что ты хочешь найти?',
    'Hello, what do you want to find?',
]
cancel_msg = [
    'Гаразд, ви покинули це меню.',
    'Ладно, вы покинули это меню.',
    'Okay, you left this menu.',
]
long_msg = [
    'Ваше повідомлення занадто довге.',
    'Ваше сообщение слишком длинное.',
    'Your message is too long.',
]
short_msg = [
    'В повідомленні має бути, щонайменше 30 символів',
    'В сообщении должно быть, по меньшей мере 30 символов',
    'The message must be at least 30 characters long',
]
message_sent = [
    'Повідомлення успішно надіслано адміністраторам.',
    'Сообщение успешно отправлено администраторам.',
    'The message was successfully sent to administrators.',
]
error_sentences = [
    'Повідомлення не пройшло перевірку. Переконайтеся, що воно є коректним.',
    'Сообщение не прошло проверку. Убедитесь, что оно является корректным.',
    'The message was not verified. Make sure it is correct.',
]
admin_ad_help = [
    'Надішли мені будь ласка рекламний текст (максимальна довжина повідомлення в Telegram - 4096 символів). Щоб вийти з цього мені нажми "Скасувати" нижче.',
    'Пришли мне пожалуйста рекламный текст (максимальная длина сообщения в Telegram - 4096 символов). Чтобы выйти из этого мне нажми "Отмена" ниже.',
    'Please send me an advertising text (the maximum length of a message in Telegram is 4096 characters). To get out of this I click "Cancel" below.',
]
contact_help = [
    'Опишіть своє питання чи побажання. Якщо у вас не встановлений псевдонім в профілі Telegram, то напишіть як з вами можна зв\'язатися. Довжина повідомлення може бути від 30 до 1000 символів. У разі якщо ви потрапили в це меню випадково, натисніть нижче "Скасувати".',
    'Опишите свой вопрос или предложение. Если у вас не установлен псевдоним в профиле Telegram, то напишите как с вами можно cвязаться. Длина сообщения может быть от 30 до 1000 символов. В случае если вы попали в это меню случайно, нажмите ниже "Отмена".',
    'Describe your question or suggestion. If you do not have a pseudonym in your Telegram profile, then write how you can be contacted. The message length can be from 30 to 1000 characters. In case you got into this menu by accident, click "Cancel" below.',
]
button_inline_error = [
    'Не вдалося отримати дані, можливо вони застаріли',
    'Не удалось получить данные, возможно они устарели',
    'Failed to retrieve data, it may be out of date',
]
ban_message = [
    'Схоже адміністрація обмежила вам доступ через порушення правил чи дуже активний темп користування (флуд).',
    'Похоже администрация ограничила вам доступ за нарушения правил или очень активный темп пользования (флуд).',
    'It looks like the administration has restricted your access for breaking the rules or for a very active rate of use (flooding).',
]
search_done_msg = [
    'За запитом "<b>%s</b>" було знайдено приблизно <b>%s</b> результатів. З них показані <b>%s</b> найбільш релевантних. (<b>%s</b> сек.)',
    'По запросу "<b>%s</b>" было найдено примерно <b>%s</b> результатов. Из них показаны <b>%s</b> наиболее релевантных. (<b>%s</b> сек.)',
    'The search query "<b>%s</b>" found approximately <b>%s</b> results. Of these, <b>%s</b> the most relevant are shown. (<b>%s</b> sec.)',
]
search_data_send_template = [
    '<a href="%s"><b>%s</b></a>\n\n%s\n\n%s',
    '<a href="%s"><b>%s</b></a>\n\n%s\n\n%s',
    '<a href="%s"><b>%s</b></a>\n\n%s\n\n%s',
]
cancel_btns = [
    'Скасувати',
    'Отмена',
    'Cancel',
]
support_btns = [
    'Допомога',
    'Помощь',
    'Help',
]
menu_btns = [
    [support_btns[0], 'Реклама'],
    [support_btns[1], 'Реклама'],
    [support_btns[2], 'Ad'],
]
news_button = [
    'Новини AWARE',
    'Новости AWARE',
    'News AWARE',
]

async def check_user_msg(string, ln) -> str:
    """
    Перевірка тексту користувача
    :param string: Строка яку потрібно перевірити
    :return: Результат
    """
    if len(string) > 1000:
        return long_msg[ln]
    elif len(string) < 29:
        return short_msg[ln]
    elif len(string.split()) < 10:
        return error_sentences[ln]
    else:
        for i in string.split():
            if len(i) > 24:
                return error_sentences[ln]