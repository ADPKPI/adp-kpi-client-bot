from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import CallbackContext
from prettytable import PrettyTable
from start_command import StartCommand
from command_base import CommandBase
from db_manager import APIClient
import logging


class StartOrderCommand(CommandBase):
    """
    Команда для ініціації процесу замовлення. Перевіряє наявність користувача в системі та ініціює процес підтвердження замовлення або реєстрацію нового користувача.
    """

    def set_factory(self, factory):
        """
        Встановлює контекст для команди. Необхідно для виклику іншої команди у процесі виконання
        """
        self.factory = factory

    def execute(self, update: Update, context: CallbackContext):
        """
        Виконує команду з ініціації замовлення.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            context.user_data['processing_order'] = True
            user_id = update.effective_user.id
            user = APIClient.get_user(user_id)
            if user:
                self.factory.get_command("request_order_confirmation").execute(update, context)
            else:
                username = update.effective_user.username
                firstname = update.effective_user.first_name
                lastname = update.effective_user.last_name
                APIClient.add_user(user_id, username, firstname, lastname)
                self.factory.get_command("request_phone_number").execute(update, context)
        except Exception as e:
            logging.error(f"Start Order Command execute error: {e}", exc_info=True)


class ConfirmOrderCommand(CommandBase):
    """
    Команда для підтвердження замовлення після збору всіх необхідних даних.
    """

    def execute(self, update: Update, context: CallbackContext):
        """
        Виконує команду підтвердження замовлення та надсилає інформацію про успішне оформлення.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            if context.user_data['processing_order']:
                context.user_data['processing_order'] = False
                user_id = update.effective_user.id
                cart_items = APIClient.get_cart(user_id)
                order_list = [(item[0], item[1], item[2]) for item in cart_items]
                total_price = sum(item[2] for item in cart_items)
                user_info = APIClient.get_user(user_id)
                phone_number = user_info[4]
                location = user_info[5]
                order_id = APIClient.create_order(user_id, phone_number, order_list, total_price, location)
                APIClient.clear_cart(user_id)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"✅ Ваше замовлення #{order_id['order_id']} оформлено. Очікуйте на дзвінок кур'єра ❣️")
            else:
                StartCommand().execute(update, context)
        except Exception as e:
            logging.error(f"Confirm Order Command execute error: {e}", exc_info=True)


class CancelOrderCommand(CommandBase):
    """
    Команда для відміни замовлення на будь-якому етапі обробки.
    """

    def execute(self, update: Update, context: CallbackContext):
        """
        Виконує команду відміни замовлення та сповіщає користувача про це.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            if context.user_data['processing_order']:
                context.user_data['processing_order'] = False
                menu_button = InlineKeyboardButton("📋 Переглянути меню", callback_data="menu")
                cart_button = InlineKeyboardButton("🧺 Перейти до кошику", callback_data="open_cart")
                context.bot.send_message(chat_id=update.effective_chat.id, text="Замовлення відхилено ❌",
                                         reply_markup=InlineKeyboardMarkup([[menu_button], [cart_button]]))
            else:
                StartCommand().execute(update, context)
        except Exception as e:
            logging.error(f"Cancel Order Command execute error: {e}", exc_info=True)


class RequestOrderConfirmationCommand(CommandBase):
    """
    Команда для запросу підтвердження замовлення, показує користувачу деталі його поточного замовлення для підтвердження.
    """

    def execute(self, update: Update, context: CallbackContext):
        """
        Виконує команду запиту на підтвердження замовлення, відображає користувачу деталі замовлення.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            if context.user_data['processing_order']:
                user_id = update.effective_user.id
                cart_items = APIClient.get_cart(user_id)
                total = sum(item[2] for item in cart_items)
                output = PrettyTable()
                output.field_names = ["Назва", "N", "Сума"]
                output.add_rows(cart_items)
                user_data = APIClient.get_user(user_id)
                location = user_data[5].split("|") if user_data and user_data[5] else (0, 0)
                latitude, longitude = map(float, location)
                order_button = InlineKeyboardButton("✅ Підтвердити замовлення", callback_data="confirm_order")
                clean_button = InlineKeyboardButton("❌ Відхилити замовлення", callback_data="cancel_order")
                menu_button = InlineKeyboardButton("🗺️ Змінити адресу", callback_data="request_location")
                keyboard = InlineKeyboardMarkup([[order_button], [clean_button], [menu_button]])
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'📄 Ваше замовлення:\n<code>{output}</code>\n\n💵 <b>До сплати:</b> {total}\n\n📱 Номер телефону: {user_data[4]}\n🗺️ Адреса доставки:',
                                         parse_mode='HTML')
                context.bot.send_location(chat_id=update.effective_chat.id, latitude=latitude, longitude=longitude,
                                          reply_markup=keyboard)
            else:
                StartCommand().execute(update, context)
        except Exception as e:
            logging.error(f"Request Order Confirmation Command execute error: {e}", exc_info=True)


class RequestPhoneNumberCommand(CommandBase):
    """
    Команда для запиту телефонного номеру користувача.
    """

    def execute(self, update: Update, context: CallbackContext):
        """
        Надсилає користувачу запит на надання свого телефонного номеру через інтерфейс Telegram.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            contact_keyboard = KeyboardButton('📱 Поділитися номером телефону', request_contact=True)
            contact_markup = ReplyKeyboardMarkup([[contact_keyboard]], one_time_keyboard=True)
            context.bot.send_message(chat_id=update.effective_chat.id, text='Будь ласка, надайте номер телефону 📱',
                                     reply_markup=contact_markup)
        except Exception as e:
            logging.error(f"Request Phone Number Command execute error: {e}", exc_info=True)


class RequestLocationCommand(CommandBase):
    """
    Команда для запиту адреси доставки у користувача.
    """

    def execute(self, update: Update, context: CallbackContext):
        """
        Вимагає від користувача надання своєї адреси через інтерфейс Telegram.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Будь ласка, вкажіть адресу доставки 🗺️\n\nTelegram -> Attach -> Location')
        except Exception as e:
            logging.error(f"Request Location Command execute error: {e}", exc_info=True)


class GotPhoneNumberCommand(CommandBase):
    """
    Обробник події отримання номера телефону від користувача.
    """

    def set_factory(self, factory):
        """
        Встановлює контекст для команди. Необхідно для виклику іншої команди у процесі виконання
        """
        self.factory = factory

    def execute(self, update: Update, context: CallbackContext):
        """
        Зберігає отриманий номер телефону і запускає наступну команду, якщо потрібно.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            if context.user_data['processing_order']:
                user_id = update.effective_user.id
                phone_number = update.message.contact.phone_number
                APIClient.update_user_contact(user_id, phone_number=phone_number)
                context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Номер збережено",
                                         reply_markup=ReplyKeyboardRemove())
                user_data = self.factory.get_command("request_location").execute(update, context)
            else:
                StartCommand().execute(update, context)
        except Exception as e:
            logging.error(f"Got Phone Number Command execute error: {e}", exc_info=True)


class GotLocationCommand(CommandBase):
    """
    Обробник події отримання адреси доставки від користувача.
    """

    def set_factory(self, factory):
        """
        Встановлює контекст для команди. Необхідно для виклику іншої команди у процесі виконання
        """
        self.factory = factory

    def execute(self, update: Update, context: CallbackContext):
        """
        Зберігає отриману адресу доставки і запускає наступну команду для підтвердження замовлення.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            if context.user_data['processing_order']:
                user_id = update.effective_user.id
                location = f"{update.message.location.latitude}|{update.message.location.longitude}"
                APIClient.update_user_contact(user_id, location=location)
                context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Адресу збережено")
                self.factory.get_command("request_order_confirmation").execute(update, context)
            else:
                StartCommand().execute(update, context)
        except Exception as e:
            logging.error(f"Got Location Command execute error: {e}", exc_info=True)
