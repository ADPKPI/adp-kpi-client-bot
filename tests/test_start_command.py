import pytest
from unittest.mock import MagicMock
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from start_command import StartCommand


def test_start_command():
    start_command = StartCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    context.user_data = {}

    start_command.execute(update, context)

    assert context.user_data['processing_order'] == False
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text=(
            'Вітаю у <b>ADP Pizza</b>! 🍕 Це ваш особистий помічник, завдяки якому ви зможете ознайомитися з нашим меню, '
            'замовити піцу та отримати інформацію про акції.\n\nСподіваємось, ви знайдете улюблені смаки та насолоджуватиметесь кожним шматочком! Cмачного! 🍕'
        ),
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Переглянути меню", callback_data="menu")],
            [InlineKeyboardButton("🧺 Перейти до кошику", callback_data="open_cart")]
        ])
    )


if __name__ == "__main__":
    pytest.main()
