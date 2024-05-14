from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from prettytable import PrettyTable
from command_base import CommandBase
from db_manager import APIClient
import logging

class AddToCartCommand(CommandBase):
    """
    Команда для додавання товару в кошик користувача.
    """
    def execute(self, product_id, update: Update, context: CallbackContext):
        """
        Виконує команду додавання товару в кошик.

        Параметри:
            product_id (int): ID товару для додавання.
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            context.user_data['processing_order'] = False
            user_id = update.effective_user.id
            menu_row = APIClient.get_pizza_details_by_id(product_id)

            if menu_row:
                APIClient.add_to_cart(user_id, product_id)
                cart_button = [[InlineKeyboardButton("🧺 Перейти до кошику", callback_data="open_cart")]]
                reply_markup = InlineKeyboardMarkup(cart_button)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Товар додано в кошик 🧺",
                                         reply_markup=reply_markup)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Товар не знайдено 😶‍🌫️")
        except Exception as e:
            logging.error(f"Add To Cart Command execute error: {e}", exc_info=True)

class OpenCartCommand(CommandBase):
    """
    Команда для перегляду кошика користувача.
    """
    def execute(self, update: Update, context: CallbackContext):
        """
        Виконує команду відкриття кошика, показуючи вміст користувача.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            context.user_data['processing_order'] = False
            user_id = update.effective_user.id
            rows = APIClient.get_cart(user_id)
            output = PrettyTable()
            output.field_names = ["Назва", "N", "Сума"]
            order_button = InlineKeyboardButton("📄 Перейти до замовлення", callback_data="start_order")
            clean_button = InlineKeyboardButton("❌ Очистити кошик", callback_data="clean_cart")
            menu_button = InlineKeyboardButton("📋 Переглянути меню", callback_data="menu")
            keyboard = [[order_button], [clean_button], [menu_button]]

            if rows:
                output.add_rows(rows)
                total = sum(row[2] for row in rows)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"<code>{output}</code>\n\n💵 <b>До сплати:</b> {total} грн",
                                         parse_mode='HTML',
                                         reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Наразі кошик пустий 😔',
                                         reply_markup=InlineKeyboardMarkup([[menu_button]]))
        except Exception as e:
            logging.error(f"Open Cart Command execute error: {e}", exc_info=True)

class CleanCartCommand(CommandBase):
    """
    Команда для очищення кошика користувача.
    """
    def execute(self, update: Update, context: CallbackContext):
        """
        Виконує команду очищення кошика.

        Параметри:
            update (Update): Об'єкт Update від Telegram API.
            context (CallbackContext): Контекст виконання команди.
        """
        try:
            context.user_data['processing_order'] = False
            user_id = update.effective_user.id
            APIClient.clear_cart(user_id)
            menu_button = InlineKeyboardButton("📋 Переглянути меню", callback_data="menu")
            context.bot.send_message(chat_id=update.effective_chat.id, text="Кошик очищено 😔",
                                     reply_markup=InlineKeyboardMarkup([[menu_button]]))
        except Exception as e:
            logging.error(f"Clean Cart Command execute error: {e}", exc_info=True)
