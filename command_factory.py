from command_handlers import *
from cart_handler import *
from order_handler import *
from start_command import StartCommand


class CommandFactory:
    """
    Фабрика команд для створення та управління різними командами в системі.

    Використовує словник для зіставлення назв команд з функціями, які створюють
    екземпляри відповідних командних об'єктів.
    """

    def __init__(self):
        """
        Ініціалізація CommandFactory з попередньо визначеним словником команд.
        """
        self.command_map = {
            "start": lambda: StartCommand(),
            "menu": lambda: MenuCommand(),
            "button_handler": lambda: self.set_command_context(ButtonHandler()),
            "details": lambda: DetailsCommand(),
            "all_details": lambda: AllDetailsCommand(),
            "add_to_cart": lambda: AddToCartCommand(),
            "open_cart": lambda: OpenCartCommand(),
            "clean_cart": lambda: CleanCartCommand(),
            "start_order": lambda: self.set_command_context(StartOrderCommand()),
            "confirm_order": lambda: ConfirmOrderCommand(),
            "cancel_order": lambda: CancelOrderCommand(),
            "request_order_confirmation": lambda: RequestOrderConfirmationCommand(),
            "request_phone_number": lambda: RequestPhoneNumberCommand(),
            "request_location": lambda: RequestLocationCommand(),
            "got_phone_number": lambda: self.set_command_context(GotPhoneNumberCommand()),
            "got_location": lambda: self.set_command_context(GotLocationCommand())
        }

    def set_command_context(self, command):
        """
        Встановлює контекст для команди, якщо це необхідно. Використовується у випадках, коли одна команда викликає іншу

        Параметри:
            command (Command): Командний об'єкт, для якого потрібно встановити контекст.

        Повертає:
            Command: Командний об'єкт з встановленим контекстом.
        """
        if hasattr(command, 'set_factory'):
            command.set_factory(self)
        return command

    def get_command(self, command_name):
        """
        Повертає екземпляр команди на основі її назви.

        Параметри:
            command_name (str): Назва команди для створення.

        Повертає:
            Command: Екземпляр команди.
        """
        command_constructor = self.command_map.get(command_name)
        if command_constructor:
            return command_constructor()
        else:
            raise ValueError(f"Unknown command: {command_name}")
