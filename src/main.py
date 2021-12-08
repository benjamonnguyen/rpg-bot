import logging
import sys

from config import configs
from src import bot
from src.managers import rest_client_session_manager


def main():
    setup()
    bot_instance = bot.build()
    bot_instance.run(configs['BOT']['TOKEN'])


def setup():
    logging.basicConfig()


# TODO handle SIGTERM refer to PomomoBeta
def handle_interrupt(signum, frame):
    # on_ready():
    #     restart_premium_sessions()
    print('Handling interrupt!', signum, frame)
    # Notify active session channels and persist premium sessions
    rest_client_session_manager.close_all()
    sys.exit(0)


if __name__ == '__main__':
    main()
