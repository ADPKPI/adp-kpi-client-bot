from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from command_factory import CommandFactory


class BotManager:
    """
    Керує всіма аспектами бота Telegram, включаючи ініціалізацію та обробку повідомлень.

    Використовує CommandFactory для управління командами, що відповідають на різні типи запитів.
    """

    def __init__(self, token):
        """
        Керує всіма аспектами бота Telegram, включаючи ініціалізацію та обробку повідомлень.

        Використовує CommandFactory для управління командами, що відповідають на різні типи запитів.
        """
        self.updater = Updater(token, use_context=True)
        self._register_handlers()

    def _register_handlers(self):
        """
        Реєструє обробники команд для різних типів повідомлень та запитів.
        """
        self.factory = CommandFactory()
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", lambda u, c: self.factory.get_command("start").execute(u, c)))
        dispatcher.add_handler(
            CommandHandler("details", lambda u, c: self.factory.get_command("details").execute(u, c), pass_args=True))
        dispatcher.add_handler(
            CallbackQueryHandler(lambda u, c: self.factory.get_command("button_handler").execute(u, c)))
        dispatcher.add_handler(
            MessageHandler(Filters.contact, lambda u, c: self.factory.get_command("got_phone_number").execute(u, c)))
        dispatcher.add_handler(
            MessageHandler(Filters.location, lambda u, c: self.factory.get_command("got_location").execute(u, c)))

    def run(self):
        """
        Запускає бота та входить в режим очікування повідомлень.
        """
        self.updater.start_polling()
        self.updater.idle()
