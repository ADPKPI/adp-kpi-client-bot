import requests
from config import api_url

class APIClient:
    """
    Клієнт API для взаємодії з веб-сервісом, що керує даними ресторану.

    Включає методи для отримання меню, деталей товарів, управління кошиком та користувачами.
    """

    @classmethod
    def get_menu(cls):
        """
        Запитує дані про всі позиції в меню.

        Returns:
            list: Список товарів у форматі JSON.
        """
        return requests.get(f"{api_url}/menu").json()

    @classmethod
    def get_pizza_details(cls, pizza_name):
        """
        Отримує деталі піци по назві.

        Parameters:
            pizza_name (str): Назва піци для пошуку деталей.

        Returns:
            dict: Деталі піци у форматі JSON.
        """
        return requests.get(f"{api_url}/menu/details/{pizza_name}").json()

    @classmethod
    def get_pizza_details_by_id(cls, product_id):
        """
        Отримує деталі піци по її унікальному ID.

        Parameters:
            product_id (int): Унікальний ID піци.

        Returns:
            dict: Деталі піци у форматі JSON.
        """
        return requests.get(f"{api_url}/menu/details-by-id/{product_id}").json()

    @classmethod
    def add_to_cart(cls, user_id, product_id):
        """
        Додає товар у кошик користувача.

        Parameters:
            user_id (int): Унікальний ID користувача.
            product_id (int): Унікальний ID товару.

        Returns:
            dict: Відповідь сервера у форматі JSON.
        """
        data = {'user_id': user_id, 'product_id': product_id}
        return requests.post(f"{api_url}/cart/add", json=data).json()

    @classmethod
    def get_cart(cls, user_id):
        """
        Отримує вміст кошика користувача.

        Parameters:
            user_id (int): Унікальний ID користувача.

        Returns:
            list: Вміст кошика у форматі JSON.
        """
        return requests.get(f"{api_url}/cart/{user_id}").json()

    @classmethod
    def clear_cart(cls, user_id):
        """
        Очищає кошик користувача.

        Parameters:
            user_id (int): Унікальний ID користувача.

        Returns:
            dict: Відповідь сервера про результат очищення кошика.
        """
        return requests.delete(f"{api_url}/cart/clear/{user_id}").json()

    @classmethod
    def get_user(cls, user_id):
        """
        Отримує інформацію про користувача за його ID.

        Parameters:
            user_id (int): Унікальний ID користувача.

        Returns:
            dict: Інформація про користувача у форматі JSON.
        """
        return requests.get(f"{api_url}/user/{user_id}").json()

    @classmethod
    def add_user(cls, user_id, username, firstname, lastname):
        """
        Реєструє нового користувача в системі.

        Parameters:
            user_id (int): Унікальний ID користувача.
            username (str): Логін користувача.
            firstname (str): Ім'я користувача.
            lastname (str): Прізвище користувача.

        Returns:
            dict: Відповідь сервера у форматі JSON.
        """
        data = {'user_id': user_id, 'username': username, 'firstname': firstname, 'lastname': lastname}
        return requests.post(f"{api_url}/user/add", json=data).json()

    @classmethod
    def update_user_contact(cls, user_id, phone_number=None, location=None):
        """
        Оновлює контактні дані користувача.

        Parameters:
            user_id (int): Унікальний ID користувача.
            phone_number (str, optional): Новий телефонний номер користувача.
            location (str, optional): Нова адреса користувача.

        Returns:
            dict: Відповідь сервера про результат оновлення даних.
        """
        data = {'user_id': user_id, 'phone_number': phone_number, 'location': location}
        return requests.patch(f"{api_url}/user/update/contact", json=data).json()

    @classmethod
    def create_order(cls, user_id, phone_number, order_list, total_price, location):
        """
        Створює нове замовлення на основі даних користувача та кошика.

        Parameters:
            user_id (int): Унікальний ID користувача.
            phone_number (str): Телефонний номер для зв'язку.
            order_list (list): Список товарів у замовленні.
            total_price (float): Загальна сума замовлення.
            location (str): Місце доставки замовлення.

        Returns:
            dict: Відповідь сервера про створення замовлення.
        """
        data = {'user_id': user_id, 'phone_number': phone_number, 'order_list': order_list, 'total_price': total_price, 'location': location}
        return requests.post(f"{api_url}/order/create", json=data).json()
