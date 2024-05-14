import pytest
from unittest.mock import MagicMock, patch
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from order_handler import StartOrderCommand, ConfirmOrderCommand, CancelOrderCommand, RequestOrderConfirmationCommand, RequestPhoneNumberCommand, RequestLocationCommand, GotPhoneNumberCommand, GotLocationCommand
from start_command import StartCommand
import re

@patch('order_handler.APIClient.get_user')
@patch('order_handler.APIClient.add_user')
def test_start_order_command(mock_add_user, mock_get_user):
    start_order_command = StartOrderCommand()
    start_order_command.set_factory(MagicMock())
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    context.user_data = {}
    mock_get_user.return_value = None
    start_order_command.execute(update, context)
    mock_get_user.assert_called_once_with(update.effective_user.id)
    mock_add_user.assert_called_once_with(
        update.effective_user.id,
        update.effective_user.username,
        update.effective_user.first_name,
        update.effective_user.last_name
    )
    start_order_command.factory.get_command.assert_called_once_with("request_phone_number")
    start_order_command.factory.get_command.return_value.execute.assert_called_once_with(update, context)

@patch('order_handler.APIClient.get_cart')
@patch('order_handler.APIClient.get_user')
@patch('order_handler.APIClient.create_order')
@patch('order_handler.APIClient.clear_cart')
def test_confirm_order_command(mock_clear_cart, mock_create_order, mock_get_user, mock_get_cart):
    confirm_order_command = ConfirmOrderCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    context.user_data = {'processing_order': True}
    mock_get_cart.return_value = [('Pizza1', 2, 200), ('Pizza2', 1, 100)]
    mock_get_user.return_value = [1, 'test_user', 'Test', 'User', '123456789', 'Test Location']
    mock_create_order.return_value = {'order_id': 1}
    confirm_order_command.execute(update, context)
    mock_get_cart.assert_called_once_with(update.effective_user.id)
    mock_get_user.assert_called_once_with(update.effective_user.id)
    mock_create_order.assert_called_once_with(
        update.effective_user.id,
        '123456789',
        [('Pizza1', 2, 200), ('Pizza2', 1, 100)],
        300,
        'Test Location'
    )
    mock_clear_cart.assert_called_once_with(update.effective_user.id)
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text="✅ Ваше замовлення #1 оформлено. Очікуйте на дзвінок кур'єра ❣️"
    )

def test_request_phone_number_command():
    request_phone_number_command = RequestPhoneNumberCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    request_phone_number_command.execute(update, context)
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text='Будь ласка, надайте номер телефону 📱',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('📱 Поділитися номером телефону', request_contact=True)]], one_time_keyboard=True)
    )

def test_request_location_command():
    request_location_command = RequestLocationCommand()
    update = MagicMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    request_location_command.execute(update, context)
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text='Будь ласка, вкажіть адресу доставки 🗺️\n\nTelegram -> Attach -> Location'
    )

@patch('order_handler.APIClient.update_user_contact')
def test_got_phone_number_command(mock_update_user_contact):
    got_phone_number_command = GotPhoneNumberCommand()
    got_phone_number_command.set_factory(MagicMock())
    update = MagicMock(spec=Update)
    update.message.contact.phone_number = '123456789'
    context = MagicMock(spec=CallbackContext)
    context.user_data = {'processing_order': True}
    got_phone_number_command.execute(update, context)
    mock_update_user_contact.assert_called_once_with(update.effective_user.id, phone_number='123456789')
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text="✅ Номер збережено",
        reply_markup=ReplyKeyboardRemove()
    )
    got_phone_number_command.factory.get_command.assert_called_once_with("request_location")
    got_phone_number_command.factory.get_command.return_value.execute.assert_called_once_with(update, context)

@patch('order_handler.APIClient.update_user_contact')
def test_got_location_command(mock_update_user_contact):
    got_location_command = GotLocationCommand()
    got_location_command.set_factory(MagicMock())
    update = MagicMock(spec=Update)
    update.message.location.latitude = 0.0
    update.message.location.longitude = 0.0
    context = MagicMock(spec=CallbackContext)
    context.user_data = {'processing_order': True}
    got_location_command.execute(update, context)
    mock_update_user_contact.assert_called_once_with(update.effective_user.id, location='0.0|0.0')
    context.bot.send_message.assert_called_once_with(
        chat_id=update.effective_chat.id,
        text="✅ Адресу збережено"
    )
    got_location_command.factory.get_command.assert_called_once_with("request_order_confirmation")
    got_location_command.factory.get_command.return_value.execute.assert_called_once_with(update, context)

if __name__ == "__main__":
    pytest.main()
