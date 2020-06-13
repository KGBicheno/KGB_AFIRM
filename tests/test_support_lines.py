import discord.ext.test as dpytest
import pytest


class TestSupportLines:

    @pytest.mark.asyncio
    async def test_support_lines(self, bot, aresponses):
        # given

        # when
        message_help = await dpytest.message("%support")

        # then
        assert message_help.content == '%support'

        message_count = dpytest.sent_queue.qsize()
        assert message_count == 8

        message_help_display = dpytest.sent_queue.get_nowait()
        assert message_help_display.content is None
        assert message_help_display.embeds is not None
        assert len(message_help_display.embeds) == 1
        assert message_help_display.embeds[0].author.name == "Mental Health Help Line"

        aresponses.assert_plan_strictly_followed()
