import logging
from typing import List

from boltons.strutils import slugify
from discord.ext import commands


class BaseBot:
    """
    The core of the bot. This class takes care of the basic bot setup and maintenance.
    """

    # these are the default
    known_cogs = [
        #'kgb_afirm.admin_and_config.admin_and_config_cog',
        'kgb_afirm.cute_times.cute_times_cog',
        'kgb_afirm.earth_and_beyond.earth_and_beyond_cog',
        'kgb_afirm.mental_health.mental_health_cog',
        'kgb_afirm.support_lines.support_lines_cog',
    ]  # type: List[str]

    # don't change discord_bot, this is to capture the bot that will be created from create_bot()
    discord_bot = None  # type: commands.Bot

    def __init__(self, bot_name: str, owner_id: int, token: str, description: str = None,
                 case_insensitive: bool = True, specified_cogs: List[str] = None, loop=None):
        """
        Create a new bot.
        Must provide the bot name, bot owner id, and bot token.
        May provide a bot description, bot sensitivity to text case, bot cogs, and bot custom loop.
        """

        self.bot_name = bot_name
        self.logger = logging.getLogger(slugify(bot_name, delim='-') + '-log')
        self.owner_id = owner_id
        self.case_insensitive = case_insensitive
        self.loop = loop
        self.token = token
        self.description = description

        if specified_cogs:
            self.known_cogs = specified_cogs

    def run_bot(self):
        """
        Run the bot.
        """

        if not self.discord_bot:
            raise ValueError("Floria has not been constructed, please call create_bot() first.")

        self.logger.info(f"Initialising {self.bot_name} ...")

        all_cogs = self.discord_bot.cogs
        self.logger.info(f"Registered Cogs: '{', '.join(sorted(all_cogs.keys()))}'")

        all_commands = self.discord_bot.commands
        self.logger.info(f"Registered Commands: '{', '.join(sorted([str(i) for i in all_commands]))}'")

        self.logger.info(f"{self.bot_name} is waking up ...")
        self.discord_bot.run(self.token)

    def create_bot(self):
        """
        Create the bot.
        """

        self.logger.info(f"Constructing {self.bot_name} ...")

        # decide the bot prefix depending on whether the message has a guild set
        def get_prefix(client, message):
            if message.guild:
                prefixes = ['%', '?', 'f.']
            else:
                prefixes = ['f.']
            return commands.when_mentioned_or(*prefixes)(client, message)

        # create the discord bot
        self.discord_bot = commands.Bot(
            command_prefix=get_prefix,
            description=self.description,
            owner_id=self.owner_id,
            case_insensitive=self.case_insensitive,
            loop=self.loop)

        # register known cogs that provide 'a collection of commands, listeners, and some state in one class'
        # See https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
        for known_cog in self.known_cogs:
            self.discord_bot.load_extension(known_cog)

        # provide cogs with access to this custom bot instance
        for cog_name, cog_instance in self.discord_bot.cogs.items():
            cog_instance.custom_bot = self
