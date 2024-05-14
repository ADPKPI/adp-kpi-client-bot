import pytest
from unittest.mock import MagicMock, patch
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from command_handlers import MenuCommand, DetailsCommand, AllDetailsCommand, ButtonHandler

@patch('command_handlers.APIClient')
def test_menu_command(mock_api_client):
    menu_command = MenuCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    mock_api_client.get_menu.return_value = [('Pizza1',), ('Pizza2',)]
    menu_command.execute(update, context)
    mock_api_client.get_menu.assert_called_once()
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text='📋 Меню <b>ADP Pizza</b>',
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Pizza1', callback_data='Pizza1')],
            [InlineKeyboardButton('Pizza2', callback_data='Pizza2')],
            [InlineKeyboardButton('Показати всі товари', callback_data='all_details')]
        ])
    )

@patch('command_handlers.APIClient')
def test_details_command(mock_api_client):
    details_command = DetailsCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    context.args = ['Pizza1']
    mock_api_client.get_pizza_details.return_value = ('Pizza1', 'Ingredients', None, 100, 1)
    details_command.execute(update, context)
    mock_api_client.get_pizza_details.assert_called_once_with('Pizza1')
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text="🍕 <b>Pizza1</b>\n\n💡 <b>Склад:</b> <i>Ingredients</i>\n\n💵 <b>Ціна:</b> 100 грн",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Додати до замовлення", callback_data="add_to_cart_1")]])
    )

    context.bot.send_message.reset_mock()
    mock_api_client.get_pizza_details.return_value = None
    details_command.execute(update, context)
    context.bot.send_message.assert_called_once_with(chat_id=update.effective_chat.id, text="Товар не знайдено 😶‍🌫️")

@patch('command_handlers.APIClient')
def test_button_handler(mock_api_client):
    button_handler = ButtonHandler()
    button_handler.set_factory(MagicMock())
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    query = MagicMock()
    update.callback_query = query
    query.data = "add_to_cart_1"
    button_handler.execute(update, context)
    button_handler.command_factory.get_command.assert_called_once_with("add_to_cart")
    add_to_cart_command = button_handler.command_factory.get_command.return_value
    add_to_cart_command.execute.assert_called_once_with("1", update, context)

if __name__ == "__main__":
    pytest.main()
