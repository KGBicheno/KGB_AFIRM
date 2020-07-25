import asyncio
import json
import os
from random import random

import gspread
from discord.ext import commands
from discord.ext.commands import Context
from oauth2client.service_account import ServiceAccountCredentials


class MentalHealthCog(commands.Cog, name='Mental Health Helper'):
	"""Sealed within are invocations for temporarily improving the mood of one who would like comfort or may need
	the attention of a mental health professional in the near future."""
	_scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
	_credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/websinthe/code/KGB_AFIRM/Credentials.json",
                                                               _scope)
	_gclient = gspread.authorize(_credentials)
	_AFFIRM_SOURCE = _gclient.open("Affirmations")
	_affirm_list = _AFFIRM_SOURCE.get_worksheet(0)

	def __init__(self, bot):
		self.bot = bot
		self.custom_bot = None

	# TODO You_are_okay() This is one of my favourite functions - write at least 50 more and pull them in from a JSON
	#  file
	@commands.command(name="notokay")
	async def You_are_okay(self, ctx: Context):
		"""If you're not feeling okay, invoke this script and I'll do my best to help you out."""
		friend = ctx.author.id
		await ctx.send("Hey, <@" + str(friend) + ">, you're okay. You're more than okay.")
		await ctx.send("You've just temporarily lost sight of how complex and unique you are. You're okay.")

	# TODO All_too_much() I love this function - write at least 50 or so and pull them from a JSON file
	@commands.command("toomuch")
	async def All_Too_Much(self, ctx: Context):
		"""If life is getting too much for you, invoke this script and I'll remind you of a few things that might
		help."""
		friend = ctx.author.id
		await ctx.send("It sounds like something's gotten you snowed under, hey <@" + str(friend) + ">?")
		await ctx.send("Just remember, you've probably felt this way before and lived to tell the tale. I  \
		                hope one day I learn how to understand what you've been through and survived. It sounds like \
		                you've got what it takes to surprise yourself.")

	@commands.command(name="thankyou")
	async def thankyou(self, ctx: Context):
		"""Invoke this script to be complemented for being amazing!"""
		complements = [
				"You are a deeply unique person, cherish that.",
				"I have a fascination for your presentation, wowsers.",
				"You're sharp as a tack, go stick it to the haters.",
				"I wish I had half your personality, it fills the room like nothing else.",
				"You're an incredible combination of luck and effort, you've done well.",
				"No one sees things the way you do, you're irreplaceable.",
				"Someone's life is incredible because of you, whether you know it or not. Thank you.",
				"I like your style",
				"In a world like this, you really cheer me up.",
				"Feeling proud of yourself is a definite option for you.",
				"If cartoon bluebirds where real, a bunch of them would be sitting on your shoulders, singing right "
				"now.",
				"You are making a difference.",
				"When you're not afraid to be yourself, is when you're most incredible.",
				"That thing you don't like about yourself, is what makes you so interesting.",
				"You're always learning things, which is awesome.",
				"You're like a breath of fresh air.",
				"Any team would be lucky to have you.",
				"You're even better than a unicorn because you're real.",
				]
		output = random.randint(1, len(complements))
		print("random: ", random.randint(1, 19))
		print("Length: ", len(complements))
		print("Output: ", output)
		print("ListOut: ", complements[output])
		await ctx.send(complements[output])

	# TODO called_affirmations() Overhaul this function to run off a JSON file instead of Google Sheets
	@commands.command(name="spoons")
	async def called_affirmation(self, ctx: Context):
		"""We all run out of spoons sometimes, and affirmations can help regain them. Invoke this script and repeat a
		psuedo-randomly chosen affirmation after me."""
		affirmations = self._affirm_list.get_all_records()
		upper = len(affirmations)
		call_affirmation_number = random.randrange(2, upper)
		self._affirm_list.update_cell(1, 8, call_affirmation_number)
		cell = self._affirm_list.cell(call_affirmation_number, 1).value
		await ctx.send("An affirmation I sometimes use is - " + cell)
		current_value = int(self._affirm_list.cell(call_affirmation_number, 5).value)
		self._affirm_list.update_cell(call_affirmation_number, 5, current_value + 1)
		return call_affirmation_number

	# TODO timed_affirmations() overhaul this function to include a larger array of breathing excercises and run off
	#  JSON instead of GS
	@commands.command(name="CalmTime")
	@commands.has_guild_permissions(manage_channels=True)
	async def timed_affirmation(self, ctx: Context):
		"""Invoking this script will start a timer. Every few minutes I'll take the channel through a breathing
		exercise and then finish with a picture of something cute."""
		while self.bot.is_ready():
			affirmations = self._affirm_list.get_all_records()
			upper = len(affirmations)
			call_affirmation_number = random.randrange(2, upper)
			self._affirm_list.update_cell(1, 8, call_affirmation_number)
			cell = self._affirm_list.cell(call_affirmation_number, 1).value
			await ctx.send("Breathe in for four ... ", delete_after=20)
			await asyncio.sleep(6)
			await ctx.send("Hold for four ... ", delete_after=20)
			await asyncio.sleep(6)
			await ctx.send("Breathe out for six ... ", delete_after=20)
			await asyncio.sleep(8)
			await ctx.send("An affirmation I sometimes use is - " + cell, delete_after=20)
			current_value = int(self._affirm_list.cell(call_affirmation_number, 5).value)
			self._affirm_list.update_cell(call_affirmation_number, 5, current_value + 1)
			with open("calm_posts.json", "r") as source:
				pic_container = json.load(source)
			pic_list = pic_container["images"]
			pic_hit = random.randrange(1, len(pic_list))
			dict_pic = pic_list[pic_hit]
			v = dict_pic.get('url')
			await asyncio.sleep(20)
			await ctx.channel.purge(limit=4)
			await asyncio.sleep(20)
			await ctx.channel.send(v)
			await ctx.channel.send("Here's some cute, I hope it helps.", delete_after=20)
			await asyncio.sleep(490)


def setup(bot):
	"""
    Register this cog as an extension.
    """
	bot.add_cog(MentalHealthCog(bot))
