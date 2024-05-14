from command_base import CommandBase
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import logging

class StartCommand(CommandBase):
    def execute(self, update: Update, context: CallbackContext):
        try:
            context.user_data['processing_order'] = False

            menu_button = InlineKeyboardButton("📋 Переглянути меню", callback_data="menu")
            cart_button = InlineKeyboardButton("🧺 Перейти до кошику", callback_data="open_cart")

            context.bot.send_message(chat_id=update.effective_chat.id,text= 'Вітаю у <b>ADP Pizza</b>! 🍕 Це ваш особистий помічник, завдяки якому ви зможете ознайомитися з нашим меню, '
                'замовити піцу та отримати інформацію про акції.\n\nСподіваємось, ви знайдете улюблені смаки та насолоджуватиметесь кожним шматочком! Cмачного! 🍕', parse_mode='HTML',
                                     reply_markup=InlineKeyboardMarkup([[menu_button], [cart_button]]))
        except Exception as e:
            logging.error(f"Start Command execute error: {e}", exc_info=True)
