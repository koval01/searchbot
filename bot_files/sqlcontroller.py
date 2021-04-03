import pymysql, logging
from config import DB_AUTH


class SQLight:

    def __init__(self) -> None:
        """
        Ініціалізація
        :return: None
        """
        logging.info('%s initialization...' % __name__)


    def get_subscriptions(self, status = True) -> dict:
        """
        Словник всіх активних користувачів
        :param status: Статус який потрібно задати
        :return: dict
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                return cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()


    def subscriber_exists(self, user_id) -> bool:
        """
        Метод перевірки наявності користувача в БД
        :param user_id: Ідентифікатор користувача
        :return: bool
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                result = cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
                return bool(len(result))


    def subscriber_get_from_user_id(self, user_id) -> dict:
        """
        Функція для отримання даних користувача за ID
        :param user_id: Ідентифікатор користувача
        :return: dict
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                result = cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
                return result


    def update_custom_field(self, user_id, field, data, two=False) -> None:
        """
        Оновлення кастомного значення в таблиці з користувачами
        :param user_id: Ідентифікатор користувача
        :param field: Колонка
        :param data: Дані
        :param two: Чи будемо додавати дані (арифметична дія)
        :return: None
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                if not two:
                    prepare_string = "UPDATE `subscriptions` SET `%s` = ? WHERE `user_id` = ?" % field
                else:
                    prepare_string = "UPDATE `subscriptions` SET `%s` = `%s` + ? WHERE `user_id` = ?" % (field, field)
                return cursor.execute(prepare_string, (data, user_id))


    def update_custom_field_payments(self, token, field, data, two=False) -> None:
        """
        Оновлення кастомного значення в платіжній таблиці
        :param token: Токен платежу
        :param field: Колонка
        :param data: Дані
        :param two: Чи будемо додавати дані (арифметична дія)
        :return: None
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                if not two:
                    prepare_string = "UPDATE `payments` SET `%s` = ? WHERE `token` = ?" % field
                else:
                    prepare_string = "UPDATE `payments` SET `%s` = `%s` + ? WHERE `token` = ?" % (field, field)
                return cursor.execute(prepare_string, (data, token))


    def add_subscriber(self, user_id, realname, status = True) -> None:
        """
        Додавання новго користувача в базу даних
        :param user_id: Ідентифікатор користувача
        :param realname: Повне ім'я профілю користувача
        :param status: Статус користувача
        :return: None
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                return cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`, `real_name`) VALUES(?,?,?)", (user_id,status,realname,))


    def add_payment(self, user_id, realname, amount, bill_id, token, bonus, status = False) -> None:
        """
        Додавання новго платежу
        :param user_id: Telegram ідентифікатор користувача
        :param realname: Ім'я та фамілія користувача
        :param amount: Сума платежу
        :param bill_id: Білінговий номер
        :param token: Токен платежу
        :param bonus: Число бонусів
        :param status: Статус платежу (За стандартом встановлюєть - неоплачений)
        :return: None
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                return cursor.execute("INSERT INTO `payments` (`user_id`, `user_name`, `amount`, `bill_id`, `token`, `bonus`, `status`) VALUES(?,?,?,?,?,?,?)", (user_id,realname,amount,bill_id,token,bonus,status,))


    def search_payment_by_token(self, token) -> dict:
        """
        Функція для отримання даних платежу за токеном
        :param token: Токен платежу
        :return: dict
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                result = cursor.execute('SELECT * FROM `payments` WHERE `token` = ?', (token,)).fetchall()
                return result


    def update_subscription(self, user_id, status=True) -> None:
        """
        Оновлення підписки визначенного користувача
        :param user_id: Ідентифікатор користувача
        :param status: Статус користувача
        :return: None
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                return cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))


    def update_lang(self, user_id, lang=1) -> None:
        """
        Оновлення мови визначенного користувача
        :param user_id: Ідентифікатор користувача
        :param lang: Мова
        :return: None
        """
        # 0 UA; 1 RU; 2 EN;
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                return cursor.execute("UPDATE `subscriptions` SET `lang` = ? WHERE `user_id` = ?", (lang, user_id))


    def update_ban(self, user_id, ban=1) -> None:
        """
        Оновлення статусу бану користувача
        :param user_id: Ідентифікатор користувача
        :param ban: Статус бану
        :return: None
        """
        # 0 unban; 1 ban;
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                return cursor.execute("UPDATE `subscriptions` SET `ban` = ? WHERE `user_id` = ?", (ban, user_id))


    def subscriber_get_lang(self, user_id) -> dict:
        """
        Функція для отримання мови користувача
        :param user_id: Ідентифікатор користувача
        :return: dict
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                result = cursor.execute('SELECT `lang` FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
                return result[0][0]


    def add_contact_ticket(self, pseudo, fullname, user_id, text) -> dict:
        """
        Додавання новго тікета
        :param pseudo: Псевдонім користувача
        :param fullname: Повне ім'я користувача
        :param user_id: Ідентифікатор користувача
        :param text: Текст повідомлення
        :return: dict
        """
        connection = pymysql.connect(host=DB_AUTH['host'], user=DB_AUTH['user'], password=DB_AUTH['password'],
                                     database=DB_AUTH['database'], cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO `contact` (`pseudo`, `fullname`, `user_id`, `text`) VALUES(?,?,?,?)", (pseudo, fullname, user_id, text,))
                result = cursor.execute('SELECT last_insert_rowid();').fetchall()
                return result
