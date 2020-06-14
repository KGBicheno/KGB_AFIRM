from logging import Logger, getLogger

from discord.ext import commands


class FloriaBot:
    """
    The core of the bot. This class takes care of the basic bot setup and maintenance.
    """

    description = 'AFIRM: Affirmations For Immediately Recomposing Mindsets | by KGB'
    bot = None  # type: commands.Bot
    token = None  # type: str
    known_cogs = [
        'kgb_afirm.support_lines.support_lines_cog',
        'kgb_afirm.earth_and_beyond.earth_and_beyond_cog'
    ]
    logger = None  # type: Logger

    def __init__(self, owner_id: int, token: str, descr: str = None, case_insensitive: bool = True, loop=None):
        """
        Create a new bot. Provide the owner id and optionally modify the description and sensitivity to text case.
        """
        self.logger = getLogger('floria-bot-log')
        self.owner_id = owner_id
        self.case_insensitive = case_insensitive
        self.loop = loop
        self.token = token

        # allow for setting a custom description
        if descr:
            self.description = descr

    def run_bot(self):
        """Run the bot."""

        if not self.bot:
            raise ValueError("Floria has not been constructed, please call create_bot() first.")

        self.logger.info(f"Initialising Floria ...")

        all_cogs = self.bot.cogs
        self.logger.info(f"Registered Cogs: '{', '.join(sorted(all_cogs.keys()))}'")

        all_commands = self.bot.commands
        self.logger.info(f"Registered Commands: '{', '.join(sorted([str(i) for i in all_commands]))}'")

        self.logger.info(f"Floria is waking up ...")
        self.bot.run(self.token)

    def create_bot(self):

        self.logger.info(f"Constructing Floria ...")

        # decide the bot prefix depending on whether the message has a guild set
        def get_prefix(client, message):
            if message.guild:
                prefixes = ['%', '?', 'f.']
            else:
                prefixes = ['f.']
            return commands.when_mentioned_or(*prefixes)(client, message)

        # create the discord bot
        self.bot = commands.Bot(
            command_prefix=get_prefix,
            description=self.description,
            owner_id=self.owner_id,
            case_insensitive=self.case_insensitive,
            loop=self.loop)

        # register known cogs that provide 'a collection of commands, listeners, and some state in one class'
        # See https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
        for known_cog in self.known_cogs:
            self.bot.load_extension(known_cog)
