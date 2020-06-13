import asyncio
import datetime
import os
from random import random

import aiohttp
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context


class EarthAndBeyondCog(commands.Cog, name='Earth and Beyond'):
    _nasa_author_icon_url = 'https://i.imgur.com/7gnuJ1z.png'
    _nasa_embed_url = 'https://i.imgur.com/Rac5kRM.png'
    _color = 0xffffff
    _error_display_text = "I'm very sorry, I'm looking up at the expanse of the universe just now. " \
                          "I might be able to show another snapshot of the wonder a little later."

    def __init__(self):
        self._nasa_api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')

    # TODO woah() Check the endpoint for description data
    #  to make the images searchable by topic and add an optional parameter
    @commands.command(name="woah")
    async def nasa_apod(self, ctx: Context):
        """
        Invoke this script to cast your eyes across the universe to behold its wonders.
        What are our problems compared to such majesty? We are part of something staggering.
        """

        await ctx.send("Aligning mirrors ...", delete_after=20)
        await asyncio.sleep(2)
        await ctx.send("Setting capture state ...", delete_after=20)

        # build url
        url = "https://api.nasa.gov/planetary/apod"
        start_date = datetime.date(1996, 1, 1)
        query_date = self._get_random_date(start_date)
        query_date_string = query_date.strftime('%Y-%m-%d')
        url_params = {
            'date': query_date_string,
            'hd': 'False',
            'api_key': self._nasa_api_key
        }

        # make request using async library
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=url_params) as response:
                if response.status == 200:
                    data = await response.json()

                    # build the discord embed and send it
                    date_date = data.get('date')
                    embed_timestamp = datetime.datetime(
                        year=query_date.year, month=query_date.month, day=query_date.day)
                    embed_display_date = embed_timestamp.strftime('%A, %d %b %Y')
                    description = data.get('description') or data.get('explanation')
                    hd_url = data.get('hdurl')
                    title = data.get('title')
                    md_url = data.get('url')
                    author_name = data.get("copyright", 'NASA Astronomy Picture of the Day')

                    embed = Embed(
                        title=title, url=self._nasa_embed_url, description=description, color=self._color,
                        timestamp=embed_timestamp)
                    embed.set_author(name=author_name, icon_url=self._nasa_author_icon_url)
                    embed.add_field(name="Date", value=embed_display_date, inline=False)
                    embed.add_field(name="HD Download", value=hd_url, inline=False)
                    embed.set_image(url=md_url)
                    embed.set_footer(text="One day, with shuffling steps, we will get there.")
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(self._error_display_text)

    #TODO nasa_mars() Look into optional arguments to have the L/R photos joined horizontally or show different cameras
    @commands.command(name="mars")
    async def nasa_mars(self, ctx: Context):
        """
        Invoke this script to scry the lands of the planet Mars through the eyes
        of the intrepid explorer, and my hero, Curiosity.
        """

        await ctx.send("Establishing interplanetary connection ...", delete_after=50)
        await asyncio.sleep(2)
        await ctx.send("Spooling up FTL signal modulator ...", delete_after=50)
        await asyncio.sleep(2)
        await ctx.send("Attempting Entanglement Twin Transfer Protocol ... ", delete_after=50)
        await asyncio.sleep(2)
        await ctx.send("Sending request for photos from NASA's Curiosity rover on Mars ...", delete_after=50)

        # build url
        url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
        start_date = datetime.date(2012, 8, 6)
        query_date = self._get_random_date(start_date)
        query_date_string = query_date.strftime('%Y-%m-%d')
        url_params = {
            'earth_date': query_date_string,
            'camera': "FHAZ",
            'api_key': self._nasa_api_key
        }

        # make request using async library
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=url_params) as response:
                if response.status == 200:
                    data = await response.json()

                    await asyncio.sleep(3)
                    await ctx.send("Response detected!", delete_after=50)

                    left_camera = data.get("photos")[0]
                    right_camera = data.get("photos")[1]

                    sol = left_camera.get("sol")
                    earth_date = left_camera.get("earth_date")
                    left_image = left_camera.get("img_src")
                    right_image = right_camera.get("img_src")

                    description = "Rover: Curiosity \n" \
                                  f"Sol {sol} \n" \
                                  f"Earth date: {earth_date} \n" \
                                  f"Two photos received, left-hand & right-hand forward hazard cameras."

                    await ctx.send(description)
                    await ctx.send(left_image)
                    await ctx.send(right_image)

                else:
                    await ctx.send(self._error_display_text)


    def _get_random_date(self, start: datetime.date, end: datetime.date = None) -> datetime.date:
        """Get a random date between start and end. End is optional and defaults to today."""
        if not end:
            end = datetime.date.today()

        start_end_delta = end - start
        random_delta = start_end_delta * random()
        random_date = start + random_delta
        return random_date


def setup(bot):
    """
    Register this cog as an extension.
    """
    bot.add_cog(EarthAndBeyondCog())
