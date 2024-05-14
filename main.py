#!/usr/bin/python3

import os
import logging
from dotenv import load_dotenv
from bot_manager import BotManager


def setup_logging():
    """
    Налаштовує логування для запису помилок у файл.

    Конфігурує базове логування, яке записує повідомлення рівня ERROR
    та вище у файл 'error.log'. Кожен запис буде містити час, рівень логування,
    і повідомлення помилки.
    """
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='error.log',
        filemode='a')


if __name__ == '__main__':
    setup_logging()

    # Завантаження змінних оточення з .env файлу
    load_dotenv()
    token = os.getenv("CLIENT_BOT_TOKEN")  # Отримання токену бота з змінних оточення

    # Створення екземпляру BotManager і запуск бота
    bot_manager = BotManager(token)
    bot_manager.run()
