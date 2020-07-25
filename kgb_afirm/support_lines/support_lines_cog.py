from importlib.resources import open_text

import yaml
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context


class SupportLinesCog(commands.Cog, name='Support Lines'):
    """
    We all need some support from time to time.
    """

    def __init__(self, bot):
        self.bot = bot
        self.custom_bot = None

    @commands.command(name="support")
    async def support_line(self, ctx: Context):
        """Support lines for mental health situations as needed. Please feel free to use them."""

        with open_text('kgb_afirm.support_lines', 'support_lines.yml') as f:
            data = yaml.safe_load(f)

            for item in data['support_lines']:
                embed = Embed(
                    title=item['title'], url=item['website_url'], description=item['description'],
                    color=item['color'])
                embed.set_author(
                    name=item['author_name'], url=item['author_website_url'], icon_url=item['author_icon_url'])
                embed.set_thumbnail(
                    url=item['thumbnail_url'])

                for field in item['fields']:
                    embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

                embed.set_footer(text=item['footer_text'])
                await ctx.send(embed=embed)


def setup(bot):
    """
    Register this cog as an extension.
    """
    bot.add_cog(SupportLinesCog(bot))
