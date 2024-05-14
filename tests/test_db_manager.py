import pytest
import requests
from unittest.mock import patch, MagicMock
from db_manager import APIClient
from config import api_url

@patch('db_manager.requests.get')
def test_get_menu(mock_get):
    mock_get.return_value.json.return_value = [{'name': 'Pizza1'}, {'name': 'Pizza2'}]
    result = APIClient.get_menu()
    mock_get.assert_called_once_with(f"{api_url}/menu")
    assert result == [{'name': 'Pizza1'}, {'name': 'Pizza2'}]

@patch('db_manager.requests.get')
def test_get_pizza_details(mock_get):
    mock_get.return_value.json.return_value = {'name': 'Pizza1', 'ingredients': 'Cheese'}
    result = APIClient.get_pizza_details('Pizza1')
    mock_get.assert_called_once_with(f"{api_url}/menu/details/Pizza1")
    assert result == {'name': 'Pizza1', 'ingredients': 'Cheese'}

@patch('db_manager.requests.get')
def test_get_pizza_details_by_id(mock_get):
    mock_get.return_value.json.return_value = {'name': 'Pizza1', 'ingredients': 'Cheese'}
    result = APIClient.get_pizza_details_by_id(1)
    mock_get.assert_called_once_with(f"{api_url}/menu/details-by-id/1")
    assert result == {'name': 'Pizza1', 'ingredients': 'Cheese'}

@patch('db_manager.requests.post')
def test_add_to_cart(mock_post):
    mock_post.return_value.json.return_value = {'status': 'success'}
    result = APIClient.add_to_cart(1, 1)
    mock_post.assert_called_once_with(f"{api_url}/cart/add", json={'user_id': 1, 'product_id': 1})
    assert result == {'status': 'success'}

@patch('db_manager.requests.get')
def test_get_cart(mock_get):
    mock_get.return_value.json.return_value = [{'product_id': 1, 'quantity': 2}]
    result = APIClient.get_cart(1)
    mock_get.assert_called_once_with(f"{api_url}/cart/1")
    assert result == [{'product_id': 1, 'quantity': 2}]

@patch('db_manager.requests.delete')
def test_clear_cart(mock_delete):
    mock_delete.return_value.json.return_value = {'status': 'success'}
    result = APIClient.clear_cart(1)
    mock_delete.assert_called_once_with(f"{api_url}/cart/clear/1")
    assert result == {'status': 'success'}

@patch('db_manager.requests.get')
def test_get_user(mock_get):
    mock_get.return_value.json.return_value = {'user_id': 1, 'username': 'test_user'}
    result = APIClient.get_user(1)
    mock_get.assert_called_once_with(f"{api_url}/user/1")
    assert result == {'user_id': 1, 'username': 'test_user'}

@patch('db_manager.requests.post')
def test_add_user(mock_post):
    mock_post.return_value.json.return_value = {'status': 'success'}
    result = APIClient.add_user(1, 'test_user', 'Test', 'User')
    mock_post.assert_called_once_with(f"{api_url}/user/add", json={'user_id': 1, 'username': 'test_user', 'firstname': 'Test', 'lastname': 'User'})
    assert result == {'status': 'success'}

@patch('db_manager.requests.patch')
def test_update_user_contact(mock_patch):
    mock_patch.return_value.json.return_value = {'status': 'success'}
    result = APIClient.update_user_contact(1, phone_number='123456789', location='Test Location')
    mock_patch.assert_called_once_with(f"{api_url}/user/update/contact", json={'user_id': 1, 'phone_number': '123456789', 'location': 'Test Location'})
    assert result == {'status': 'success'}

@patch('db_manager.requests.post')
def test_create_order(mock_post):
    mock_post.return_value.json.return_value = {'status': 'success'}
    result = APIClient.create_order(1, '123456789', [{'product_id': 1, 'quantity': 2}], 200.0, 'Test Location')
    mock_post.assert_called_once_with(f"{api_url}/order/create", json={
        'user_id': 1,
        'phone_number': '123456789',
        'order_list': [{'product_id': 1, 'quantity': 2}],
        'total_price': 200.0,
        'location': 'Test Location'
    })
    assert result == {'status': 'success'}

if __name__ == "__main__":
    pytest.main()
