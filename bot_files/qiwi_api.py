from urllib.parse import urlunsplit, urlencode
from api_module import get_random_string
from config import qiwi_api_key, qiwi_api_key_secret, default_limit, cut_price
import aiohttp, json


async def create_payment_url(amount, bot_pseudo, db, message, bonus, comment=None) -> dict:
    """
    Запит до QIWI для стоврення платежу
    :param amount: Сума платежу в рублях
    :param bot_pseudo: Псевдонім бота для генерації посилання
    :param db: Клас для роботи з базою даних
    :param message: Тіло отриманого повідомлення від користувача
    :param bonus: Число бонусів
    :param comment: Коментар платежу (ідентифікатор)
    :return: JSON відповідь переведена в словник
    """
    SC = 'https'
    DOMAIN = 'oplata.qiwi.com'
    PATH = '/create'
    token = await get_random_string(40)
    s_url = 'https://t.me/%s/?start=%s' % (bot_pseudo, token)
    bill = await get_random_string(199)
    if not comment:
        comment = 'Увеличение ежедневной квоты поиска для бота AWARE (Token: %s)' % token
    query = urlencode(dict(
        publicKey=qiwi_api_key,
        billId=bill,
        amount=amount,
        comment=comment,
        successUrl=s_url,
    ))
    db.add_payment(
        message.from_user.id,
        message.from_user.full_name,
        amount, bill, token, bonus
    )
    return dict(
        billid=bill,
        amount=amount,
        url=urlunsplit((SC, DOMAIN, PATH, query, "")),
    )


async def check_payment(billid) -> dict:
    """
    Запит до QIWI для перевірки платежу
    :param billid: Номер платежу (Ідентифікатор)
    :return: JSON відповідь
    """
    url = f"https://api.qiwi.com/partner/bill/v1/bills/{billid}"
    for i in range(1):
        async with aiohttp.request('GET', url, headers={
            "Authorization": f"Bearer {qiwi_api_key_secret}",
            "Accept": "application/json",
        }) as response:
            if response.status == 200 and await response.text():
                return json.loads(await response.text())


async def verify_payment(token, db) -> str:
    """
    Перевірка платежу
    :param token: Номер платежу (Ідентифікатор)
    :return: Cтрока в якій вказана помилка
    """
    payment = db.search_payment_by_token(token)[0]
    billid = payment[4]
    amount = payment[3]
    data = await check_payment(billid) # Отримуємо інформацію про платіж
    ok = 'PAID'
    wait = 'WAITING'
    if data:
        if round(float(data['amount']['value'])) == amount:
            if data['status']['value'] == ok:
                return 'Успех!'
            elif data['status']['value'] == wait:
                return 'Ошибка подтверждения. Платеж не было завершено / оплачено.'
            else:
                return 'Ошибка подтверждения. Платеж не найден или он недействительный.'
        else:
            return 'Сумма платежа неверна. Похоже, пользователь её изменил.'


async def get_amount_pay(bonus) -> dict:
    """
    Визначення суми платежу
    :param bonus: Кількість бонусу
    :return: dict price
    """
    x = round((bonus * 1.4) * (default_limit / cut_price))
    default = default_limit + bonus
    return dict(
        bonuses=bonus,
        rub_price=x,
        new_limit=default
    )