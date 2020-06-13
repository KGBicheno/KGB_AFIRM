from discord.ext import commands


class FloriaBot:
    """
    The core of the bot. This class takes care of the basic bot setup and maintenance.
    """

    description = 'AFIRM: Affirmations For Immediately Recomposing Mindsets | by KGB'
    bot = None  # type: commands.Bot
    known_cogs = [
        'kgb_afirm.support_lines.support_lines_cog',
        'kgb_afirm.earth_and_beyond.earth_and_beyond_cog'
    ]

    def __init__(self, owner_id: int, descr: str = None, case_insensitive: bool = True, loop=None):
        """
        Create a new bot. Provide the owner id and optionally modify the description and sensitivity to text case.
        """

        # allow for setting a custom description
        if descr:
            self.description = descr

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
            owner_id=owner_id,
            case_insensitive=case_insensitive,
            loop=loop)

        # register known cogs that provide 'a collection of commands, listeners, and some state in one class'
        # See https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
        for known_cog in self.known_cogs:
            self.bot.load_extension(known_cog)


