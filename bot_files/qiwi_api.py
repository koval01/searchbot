from urllib.parse import urlunsplit, urlencode
from api_module import get_random_string
from config import qiwi_api_key, qiwi_api_key_secret
import aiohttp, json


async def create_payment_url(amount, bot_pseudo, token, comment=None) -> dict:
    """
    Запит до QIWI для стоврення платежу
    :param amount: Сума платежу в рублях
    :param bot_pseudo: Псевдонім бота для генерації посилання
    :param token: Ідентифікатор платежу для його перевірки
    :param comment: Коментар платежу (ідентифікатор)
    :return: JSON відповідь переведена в словник
    """
    SC = 'https'
    DOMAIN = 'oplata.qiwi.com'
    PATH = '/create'
    s_url = 'https://t.me/%s/?start=%s' % (bot_pseudo, token)
    bill = await get_random_string(199)
    if not comment:
        comment = 'Увеличение ежедневной квоты поиска для бота AWARE'
    query = urlencode(dict(
        publicKey=qiwi_api_key,
        billId=bill,
        amount=amount,
        comment=comment,
        successUrl=s_url,
    ))
    return dict(
        billid=bill,
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


async def verify_payment(billid, amount) -> str:
    """
    Перевірка платежу
    :param billid: Номер платежу (Ідентифікатор)
    :param amount: Сума яку користувач повинен був заплатити
    :return: Булентний результат або строка в якій вказана помилка
    """
    data = await check_payment(billid) # Отримуємо інформацію про платіж
    ok = 'PAID'
    wait = 'WAITING'
    if data:
        if data['amount']['value'] == amount:
            if data['status']['value'] == ok:
                return True
            elif data['status']['value'] == wait:
                return 'Ошибка подтверждения. Платеж не было завершено / оплачено.'
            else:
                return 'Ошибка подтверждения. Платеж не найден или он недействительный.'
        else:
            return 'Сумма платежа неверна. Похоже, пользователь её изменил.'

    return False