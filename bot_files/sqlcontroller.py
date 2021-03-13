import sqlite3, logging, asyncio


class SQLight:

    def __init__(self, database) -> None:
        """
        Ініціалізація
        :return: None
        """
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

        logging.info('%s initialization...' % __name__)
        logging.info('%s database file' % database)


    def get_subscriptions(self, status = True) -> dict:
        """
        Словник всіх активних користувачів
        :return: dict
        """
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()


    def subscriber_exists(self, user_id) -> bool:
        """
        Метод перевірки наявності користувача в БД
        :return: bool
        """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))


    def subscriber_get_from_user_id(self, user_id) -> dict:
        """
        Функція для отримання даних користувача за ID
        :return: dict
        """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return result


    def add_subscriber(self, user_id, realname, status = True) -> None:
        """
        Додавання новго користувача
        :return: None
        """
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`, `real_name`) VALUES(?,?,?)", (user_id,status,realname,))


    def update_subscription(self, user_id, status=True) -> None:
        """
        Оновлення підписки визначенного користувача
        :return: None
        """
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))


    def add_contact_ticket(self, pseudo, fullname, user_id, text) -> dict:
        """
        Додавання новго тікета
        :param pseudo: Псевдонім користувача
        :param fullname: Повне ім'я користувача
        :param user_id: Ідентифікатор користувача
        :param text: Текст повідомлення
        :return: dict
        """
        with self.connection:
            self.cursor.execute("INSERT INTO `contact` (`pseudo`, `fullname`, `user_id`, `text`) VALUES(?,?,?,?)", (pseudo, fullname, user_id, text,))
            result = self.cursor.execute('SELECT last_insert_rowid();').fetchall()
            return result
