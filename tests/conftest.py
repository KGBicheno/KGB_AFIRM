import pytest
import discord.ext.test as dpytest
from kgb_afirm.floria_bot import FloriaBot


# conftest.py contains fixtures that are available to all tests
# use them by using the name of the function as a parameter in a test
# See https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions


@pytest.fixture
def bot(caplog, event_loop):
    bot = FloriaBot(owner_id=123456789, token='987654321', loop=event_loop)
    bot.create_bot()
    dpytest.configure(bot.discord_bot)
    yield bot
    dpytest.sent_queue.empty()
