from urllib.parse import urlunsplit, urlencode
from api_module import get_random_string
from config import qiwi_api_key


async def create_payment_url(amount, comment, bot_pseudo, token) -> dict:
    """
    Запит до QIWI для стоврення платежу
    :param amount: Сума платежу в рублях
    :param comment: Коментар платежу (ідентифікатор)
    :param bot_pseudo: Псевдонім бота для генерації посилання
    :param token: Ідентифікатор платежу для його перевірки
    :return: JSON відповідь переведена в словник
    """
    SC = 'https'
    DOMAIN = 'oplata.qiwi.com'
    PATH = '/create'
    s_url = 'https://t.me/%s/?start=%s' % (bot_pseudo, token)
    bill = await get_random_string(199)
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


# async def create_payment(amount, comment, bot_pseudo, token) -> dict:
#     """
#     Запит до QIWI для стоврення платежу
#     :param question: Текст запитання
#     :return: JSON відповідь переведена в словник
#     """
#     url = 'https://oplata.qiwi.com/create'
#     s_url = 'https://t.me/%s/?start=%s' % (bot_pseudo, token)
#     for i in range(3):
#         async with aiohttp.request('GET', url, params={
#             "publicKey": qiwi_api_key,
#             "billId": get_random_string(192),
#             "amount": amount,
#             "comment": comment,
#             "successUrl": s_url,
#         }) as response:
#             if response.status == 200 and await response.text():
#                 return json.loads(await response.text())