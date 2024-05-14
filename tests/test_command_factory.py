import pytest
from command_factory import CommandFactory
from start_command import StartCommand
from cart_handler import AddToCartCommand
from order_handler import ConfirmOrderCommand, CancelOrderCommand
from command_handlers import ButtonHandler

def test_get_command():
    factory = CommandFactory()

    command = factory.get_command("start")
    assert isinstance(command, StartCommand)

    command = factory.get_command("add_to_cart")
    assert isinstance(command, AddToCartCommand)

    command = factory.get_command("confirm_order")
    assert isinstance(command, ConfirmOrderCommand)

    command = factory.get_command("cancel_order")
    assert isinstance(command, CancelOrderCommand)

    with pytest.raises(ValueError):
        factory.get_command("unknown_command")

if __name__ == "__main__":
    pytest.main()
