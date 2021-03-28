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
news_error_get = [
    'Виникла помилка при формуванні стрічки новин.',
    'Возникла ошибка при формировании ленты новостей.',
    'There was an error forming the news feed.',
]
news_no = [
    'Пробач, але стрічку новин не можна оновлювати частіше ніж раз в дві години. Це зроблено для запобігання флуду. Якщо Ви відправите запит раніше, то таймер скинеться.',
    'Извините, но новостная лента не может обновляться чаще одного раза в два часа. Это сделано, чтобы предотвратить флуд. Если Вы отправите запрос раньше, то таймер сбросится.',
    'Sorry, but the news feed cannot be updated more than once every two hours. This is done to prevent flooding. If you send a request earlier, the timer will reset.',
]
news_template = [
    '<b>%s</b>\n\n%s\n\nДжерело: <a href="%s"><b>%s</b></a>',
    '<b>%s</b>\n\n%s\n\nИсточник: <a href="%s"><b>%s</b></a>',
    '<b>%s</b>\n\n%s\n\nSource: <a href="%s"><b>%s</b></a>',
]
news_scroll = [
    'Наступна новина',
    'Следующая новость',
    'Next news',
]
news_slowly = [
    'Повільніше будь ласка',
    'Медленнее пожалуйста',
    'Slower please',
]
no_news_more = [
    'Можливо виникла помилка, запитайте новини ще раз.',
    'Возможно возникла ошибка, запросите новости еще раз.',
    'An error may have occurred, request the news again.',
]
ban_user_notify = 'The %s administrator has blocked the user %s'
already_banned = [
    'Користувач вже заблокований',
    'Пользователь уже заблокирован',
    'User is already blocked',
]
already_unbanned = [
    'Схоже цей користувач вже розблокований',
    'Похоже этот пользователь уже разблокирован',
    'It looks like this user is already unlocked',
]
news_view_finish_notify = [
    'Ви переглянули всі новини на сьогодні. Буду радий бачити Вас завтра 😉',
    'Вы просмотрели все новости на сегодня. Буду рад видеть Вас завтра 😉',
    'You have viewed all the news for today. I will be glad to see you tomorrow 😉',
]
news_view_finish_button = [
    'Гаразд, дякую',
    'Ладно, спасибо',
    'Okay, thanks',
]
weather_feel_temp = [
    'Відчувається, як',
    'Чувствуется, как',
    'Feels like',
]
weather_pressure = [
    'Тиск',
    'Давление',
    'Pressure',
]
weather_pressure_m = [
    'гПа',
    'гПа',
    'hPa',
]
weather_humidity = [
    'Вологість',
    'Влажность',
    'Humidity',
]
weather_temp = [
    'Температура',
    'Температура',
    'Temperature',
]
weather_wind = [
    'Вітер',
    'Ветер',
    'Wind',
]
limit_search_msg = [
    'Пробач, але на сьогодні твоя квота на пошуки вичерпана. (/limit)',
    'Прости, но на сегодня твоя квота на поиски исчерпана. (/limit)',
    'I\'m sorry, but your quota for searches has been exhausted. (/limit)',
]
limit_menu_msg = [
    'Привіт, ти маєш 50 безкоштовних пошуків, та %s бонусних. За сьогодні використано %s. Отже до вичерпання квоти на сьогодні, залишилося %s пошуків.',
    'Привет, ты имеешь 50 бесплатных поисков, и %s бонусных. За сегодня использовано %s. К исчерпанию квоты на сегодня осталось %s поисков.',
    'Hi, you have 50 free searches and %s bonuses. %s used today. So until the quota is exhausted today, there are %s searches left.',
]
pay_info = [
    'Гаразд, після оплати тебе буде перенаправлено на сторінку t.me/%s/?start=XXXXXXXXXXX, після цього потрібно буде перейти в чат з ботом через цю сторінку. У параметрі start вказано код вашого оплаченого замовлення, ти можеш використовувати це посилання в якості подарункового, тому не передавай його нікому до тих пір, поки не використаєш.',
    'Ладно, после оплаты тебя будет перенаправлено на страницу t.me/%s/?start=XXXXXXXXXXX, после этого нужно будет перейти в чат с ботом через эту страницу. В параметре start указан код вашего оплаченного заказа, ты можешь использовать эту ссылку в качестве подарочной, поэтому не передавай её никому до тех пор, пока не используешь.',
    'Okay, after payment you will be redirected to the page t.me/%s/?start=XXXXXXXXXXX, after that you will need to go to the chat with the bot through this page. The start parameter contains the code of your paid order, you can use this link as a gift, so do not give it to anyone until you use it.',
]
pay_check = [
    'Сума: %s\nБонус: %s\n\nНе забудь зберегти чек, він потрібен на випадок невдалої автоматичної перевірки платежу.',
    'Сумма: %s\nБонус: %s\n\nНе забудь сохранить чек, он нужен на случай неудачной автоматической проверки платежа.',
    'Sum: %s\nBonus: %s\n\nDo not forget to save the check, it is needed in case of failure of automatic verification of payment.',
]
payment_create = [
    'Вкажіть потрібну вам кількість додаткових пошуків',
    'Укажите нужное вам количество дополнительных поисков',
    'Specify the number of additional searches you need',
]
help_menu_msg = [
    '/limit - Інформація про обмеження\n/bonus - Збільшити квоту\n/lang - Змінити мову',
    '/limit - Информация об ограничении\n/bonus - Увеличить квоту\n/lang - Изменить язык',
    '/limit - Restriction information\n/bonus - Increase quota\n/lang - Change language',
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