import discord.ext.test as dpytest
import pytest

from kgb_afirm.floria_bot import FloriaBot

class TestBasic:

    @pytest.mark.asyncio
    async def test_bot_help(self, bot, aresponses):
        # given

        # when
        message_help = await dpytest.message("%help")

        # then
        assert message_help.content == '%help'

        message_count = dpytest.sent_queue.qsize()
        message_help_display = dpytest.sent_queue.get_nowait()

        assert message_count == 1

        assert bot.description in message_help_display.content

        assert "Support Lines" in message_help_display.content
        assert "support Support lines for mental health situations as needed." in message_help_display.content

        assert "Earth and Beyond" in message_help_display.content

        aresponses.assert_plan_strictly_followed()
