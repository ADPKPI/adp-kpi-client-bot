import pytest
from unittest.mock import MagicMock, patch
from cart_handler import AddToCartCommand, OpenCartCommand, CleanCartCommand
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

@patch('cart_handler.APIClient')
def test_add_to_cart_command(mock_api_client):
    add_to_cart = AddToCartCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)

    # Настройка mock для метода APIClient.get_pizza_details_by_id
    mock_api_client.get_pizza_details_by_id.return_value = True

    # Тест на успешное добавление товара в корзину
    add_to_cart.execute(1, update, context)
    mock_api_client.add_to_cart.assert_called_once_with(update.effective_user.id, 1)
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text="Товар додано в кошик 🧺",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🧺 Перейти до кошику", callback_data="open_cart")]])
    )

    # Тест на случай, когда товар не найден
    context.bot.send_message.reset_mock()
    mock_api_client.get_pizza_details_by_id.return_value = None
    add_to_cart.execute(1, update, context)
    context.bot.send_message.assert_called_once_with(chat_id=update.effective_chat.id, text="Товар не знайдено 😶‍🌫️")

@patch('cart_handler.APIClient')
def test_open_cart_command(mock_api_client):
    open_cart = OpenCartCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)

    # Настройка mock для метода APIClient.get_cart
    mock_api_client.get_cart.return_value = [('Товар1', 2, 200), ('Товар2', 1, 100)]

    # Тест на успешное открытие корзины с товарами
    open_cart.execute(update, context)
    mock_api_client.get_cart.assert_called_once_with(update.effective_user.id)
    context.bot.send_message.assert_called_once()
    assert "До сплати" in context.bot.send_message.call_args[1]['text']

    # Тест на случай, когда корзина пустая
    context.bot.send_message.reset_mock()
    mock_api_client.get_cart.return_value = []
    open_cart.execute(update, context)
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text='Наразі кошик пустий 😔',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 Переглянути меню", callback_data="menu")]])
    )

@patch('cart_handler.APIClient')
def test_clean_cart_command(mock_api_client):
    clean_cart = CleanCartCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)

    # Тест на успешное очищение корзины
    clean_cart.execute(update, context)
    mock_api_client.clear_cart.assert_called_once_with(update.effective_user.id)
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text="Кошик очищено 😔",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 Переглянути меню", callback_data="menu")]])
    )

if __name__ == "__main__":
    pytest.main()
