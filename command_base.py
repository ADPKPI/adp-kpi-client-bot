from telegram import Update
from telegram.ext import CallbackContext


class CommandBase:
    """
    Абстрактний базовий клас для всіх команд бота.

    Визначає інтерфейс для виконання команд, що мають бути імплементовані
    в похідних класах.
    """

    def execute(self, update: Update, context: CallbackContext):
        """
        Абстрактний метод для виконання команди бота.

        Призначений для перевизначення в похідних класах, де реалізовується
        специфічна логіка обробки відповідної команди.

        Параметри:
            update (Update): Об'єкт Update від Telegram API, який містить інформацію про вхідне повідомлення.
            context (CallbackContext): Контекст виконання команди, що надає засоби та можливості для управління даними та станом в межах сеансу.

        Піднімає:
            NotImplementedError: Якщо метод не був перевизначений у похідному класі.
        """
        raise NotImplementedError("Subclasses must implement this method")
