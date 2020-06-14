import os
import sys
from logging import config, getLogger


from kgb_afirm.floria_bot import FloriaBot


def get_env_var(name: str):
    """Check that an env var exists, and get the value."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"An environment variable is missing, please set '{name}'.")
    return value


def run_floria():
    """Run the Floria bot."""

    # used by a discord.py Cog
    get_env_var('NASA_API_KEY')

    # get settings for the Floria bot
    discord_owner_id = int(get_env_var('KGB_AFIRM_FLORIA_DISCORD_OWNER_ID'))
    discord_token = get_env_var('KGB_AFIRM_FLORIA_DISCORD_TOKEN')

    # create an instance of the FloriaBot class
    bot = FloriaBot(owner_id=discord_owner_id, token=discord_token)

    # start the bot
    bot.create_bot()
    bot.run_bot()


def configure_logging():
    # configure logging - log to both a file (discord.log) and the console.
    config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)-8s [%(name)s] %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'log_file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': 'discord.log',
                'encoding': 'utf-8',
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'log_file']
        }
    })

    def handle_exception(exc_type, exc_value, exc_traceback):
        """
        Capture unhandled exceptions so they can be logged.
        From https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
        """

        # Ignore KeyboardInterrupt so a console python program can exit with Ctrl + C.
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        getLogger('kbg-afirm-log').critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    # install the unhandled exception logger
    sys.excepthook = handle_exception


# for when this file is run directly as a script
if __name__ == '__main__':
    configure_logging()

    # start floria
    run_floria()


# -- Install require packages --
# pip install -U aiohttp discord.py yaml

# -- Tests --
# installing packages for tests: pip install -U dpytest pytest coverage

# To run tests, change directory to the top level of this repo, and run: pytest

# Then run the tests with coverage enabled: coverage run -m pytest
# Have a look at the basic report: coverage report -m
# Generate the html report: coverage html
# Then open the html report, it is at htmlcov/index.html
