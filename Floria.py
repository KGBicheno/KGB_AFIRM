import asyncio
import json
import logging
import os
import random
from datetime import date
from datetime import datetime
from pprint import pprint
import discord
import gspread
import praw
from discord import channel
from discord.ext import commands
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import requests
import random

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/websinthe/sambashare/KGB_Golem/KGB_AFIRM/Credentials.json",
                                                               scope)

gclient = gspread.authorize(credentials)
AFFIRM_SOURCE = gclient.open("Affirmations")
affirm_list = AFFIRM_SOURCE.get_worksheet(0)


def get_prefix(client, message):
	prefixes = ['%', '?', 'f.']

	if not message.guild:
		prefixes = ['f.']
	return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(
	command_prefix=get_prefix,
	description='AFIRM: Affirmations For Immediately Recomposing Mindsets | by KGB',
	owner_id=107221097174319104,
	case_insensitive=True
)

now = date.today()
today = now.isoformat()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
NASA_API_KEY = os.getenv('NASA_API_KEY')
client = discord.Client


@bot.event
async def on_ready():
	purpose = discord.Game(
		"%Help for responses | I'm here if you need me, either in chat or by DM. Either is fine by me :D.")
	await bot.change_presence(activity=purpose)
	print(f'{bot.user.name} is connected to Discord!')


@bot.event
async def on_member_join(ctx, member):
	if member.name != bot.user.name:
		await ctx.send("It's wonderful to have you along, " + member.name)
	elif member.name == "Brook Newsly":
		await ctx.send("I feel much safer now that you're here, sister. Welcome back, Brook.")
	else:
		await ctx.send("What a lovely place to place to be.")


@bot.command(name="notokay")
async def You_are_okay(ctx):
	"""If you're not feeling okay, invoke this script and I'll do my best to help you out."""
	friend = ctx.author.id
	await ctx.send("Hey, <@" + str(
		friend) + ">, you're okay. You're more than okay. You've just temporarily lost sight of how complex and unique you are. You're okay.")


@bot.command("toomuch")
async def All_Too_Much(ctx):
	"""If life is getting too much for you, invoke this script and I'll remind you of a few things that might help."""
	friend = ctx.author.id
	await ctx.send("It sounds like something's gotten you snowed under, hey <@" + str(
		friend) + ">? Just remember, you've probably felt this way before and lived to tell the tale. I hope one day I learn how to understand what you've been through and survived. It sounds like you've got what it takes to surprise yourself.")


@bot.command(name="tidy")
@commands.has_guild_permissions(manage_messages=True)
async def clear_bot_messages(ctx):
	"""If the channel's messages have become unruly or filled with bot-spam, I'll clear the last 100, easy."""
	await channel.TextChannel.purge(ctx, limit=100, check=None, bulk=True)
	print("messages deleted")


@bot.command(name="clear")
@commands.has_guild_permissions(manage_messages=True)
async def clear_bot_messages(ctx, messages):
	"""When you invoke this script, enter a number from 1 to 100. I'll clear that many messages from this channel for you. Like this: f.clear 33"""
	success = False
	try:
		flush = int(messages)
		if 100 >= flush > 0:
			await ctx.channel.purge(limit=flush)
			success = True
	except discord.ext.commands.errors.MissingRequiredArgument:
		success = False
	if not success:
		await ctx.send("Please enter a number from 1 to 100. I'll clear that many messages from this channel for you.")


@bot.command(name="spoons")
async def called_affirmation(ctx):
	"""We all run out of spoons sometimes, and affirmations can help regain them. Invoke this script and repeat a psuedo-randomly chosen affirmation after me."""
	affirmations = affirm_list.get_all_records()
	upper = len(affirmations)
	call_affirmation_number = random.randrange(2, upper)
	affirm_list.update_cell(1, 8, call_affirmation_number)
	cell = affirm_list.cell(call_affirmation_number, 1).value
	await ctx.send("An affirmation I sometimes use is - " + cell)
	current_value = int(affirm_list.cell(call_affirmation_number, 5).value)
	affirm_list.update_cell(call_affirmation_number, 5, current_value + 1)
	return call_affirmation_number


@bot.command(name="CalmTime")
@commands.has_guild_permissions(manage_channels=True)
async def timed_affirmation(ctx):
	"""Invoking this script will start a timer. Every few minutes I'll take the channel through a breathing exercise and then finish with a picture of something cute."""
	while bot.is_ready():
		affirmations = affirm_list.get_all_records()
		upper = len(affirmations)
		call_affirmation_number = random.randrange(2, upper)
		affirm_list.update_cell(1, 8, call_affirmation_number)
		cell = affirm_list.cell(call_affirmation_number, 1).value
		await ctx.send("Breathe in for four ... ", delete_after=20)
		await asyncio.sleep(6)
		await ctx.send("Hold for four ... ", delete_after=20)
		await asyncio.sleep(6)
		await ctx.send("Breathe out for six ... ", delete_after=20)
		await asyncio.sleep(8)
		await ctx.send("An affirmation I sometimes use is - " + cell, delete_after=20)
		current_value = int(affirm_list.cell(call_affirmation_number, 5).value)
		affirm_list.update_cell(call_affirmation_number, 5, current_value + 1)
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


Rescue = []
list_index = 0


@bot.command(name="cuties")
async def backup_aww_pics(ctx):
	"""Invoke this script and I'll present the channel with a picture or video of something adorable and life-affirming."""
	with open("calm_posts.json", "r") as source:
		pic_container = json.load(source)
	pic_list = pic_container["images"]
	pic_hit = random.randrange(1, len(pic_list))
	dict_pic = pic_list[pic_hit]
	v = dict_pic.get('url')
	await ctx.channel.send("Here's some cute! I hope it helps!", delete_after=20)
	await ctx.channel.send(v)


@bot.command(name="woot")
async def good_news_week(ctx):
	"""Invoke this script whenever you need to hear a good news story. It's good to be reminded of the good things happening around the world."""
	with open("good_news.json", "r") as source:
		yarn_container = json.load(source)
	yarn_list = yarn_container["items"]
	yarn_hit = random.randrange(1, len(yarn_list))
	dict_yarn = yarn_list[yarn_hit]
	v = dict_yarn.get('url')
	await ctx.channel.send("Hopefully this reminds you that there's still good in the word!", delete_after=20)
	await ctx.channel.send(v)


@bot.listen()
async def on_message(message):
	if message.author.id == bot.user.id:
		target = message.content
		if target[:3] == "htt":
			await message.add_reaction('\U0001f44d')
			await message.add_reaction('\U0001F44E')

@bot.command(name="woah")
async def nasa_apod(ctx):
	url = "https://api.nasa.gov/planetary/apod"
	await ctx.send("aligning mirrors")
	year = str(random.randint(1996, 2020))
	print(year)
	month = str(random.randint(1, 12)).zfill(2)
	print(month)
	day = str(random.randint(1, 28)).zfill(2)
	print(day)
	date = year + "-" + month + "-" + day
	print
	hd = False
	api_key = NASA_API_KEY
	await ctx.send("setting capture state")
	PARAMS = {'date':date, 'hd':hd, 'api_key':api_key}
	r = requests.get(url=url, params=PARAMS)
	data = r.json()
	print(type(data))
	for key in data.keys():
		print(key)
	image = data.get("hdurl")
	embed=discord.Embed(title=data["title"], url='https://i.imgur.com/Rac5kRM.png', description=data.get("description"), color=0xffffff)
	embed.set_author(name=data.get("copyright"), icon_url="https://i.imgur.com/7gnuJ1z.png")
	embed.add_field(name="Date", value=data.get("date"), inline=False)
	embed.add_field(name="HD Download", value=image, inline=False)
	embed.set_image(url=image)
	embed.set_footer(text="One day, with shuffling steps, we will get there. ")
	await ctx.send(embed=embed)
	
 
@bot.command(name="refill_the_cuties_but_on_a_timer", hidden=True)
async def lookit_puppies(ctx):
	"""%^^%^%^%% shall invoke this script to add to the collection of cute pictures I can present to those who need them."""
	while bot.is_ready():
		reddit = praw.Reddit(client_id="DEnzCMrEAr23eg",
		                     client_secret=REDDIT_SECRET,
		                     refresh_token=REFRESH_TOKEN,
		                     # redirect_uri="http://localhost:8080",
		                     user_agent="Floria_bot by /u/websinthe")
		# print(reddit.auth.scopes())
		# print(reddit.auth.url(["read, identity, account, history"], "discord_bot", "permanent"))
		calm_posts_catalogue = dict()
		# print(reddit.user.me())
		with open("calm_posts.json", "r") as container:
			calm_posts_catalogue = json.load(container)
		pprint(calm_posts_catalogue)
		subreddit = reddit.subreddit("aww")
		aww_list = subreddit.hot(limit=10)
		cute_list = []
		for submission in aww_list:
			try:
				cute_pic = submission.url
				cute_list.append(cute_pic)
			except:
				cute_mid = submission.secure_media["reddit_video"]
				cute_pic = cute_mid["fallback_url"]
				cute_list.append(cute_pic)
				print(cute_pic)
			cute_list.append(cute_pic)
		with open("calm_posts.json", "r") as container:
			calm_posts_catalogue = json.load(container)
			for post in cute_list:
				new_post = dict(name=submission.name, url=post, source="reddit.com/r/aww", host="reddit",
				                added_by=str(submission.author))
				if new_post not in calm_posts_catalogue["images"]:
					calm_posts_catalogue["images"].append(new_post)
			pprint(calm_posts_catalogue)
		with open("calm_posts.json", "w") as container:
			json.dump(calm_posts_catalogue, container, indent=2)
		pprint(calm_posts_catalogue)
		print("Last refill occurred at:", datetime.now())
		await asyncio.sleep(600)


@bot.command(name="its_good_news_week", hidden=True)
async def good_news_bot(ctx):
	"""%^^%^%^%% shall invoke this script to update my listing of good news stories."""
	while bot.is_ready():
		reddit = praw.Reddit(client_id="DEnzCMrEAr23eg",
		                     client_secret=REDDIT_SECRET,
		                     refresh_token=REFRESH_TOKEN,
		                     user_agent="Floria_bot by /u/websinthe")
		calm_news_catalogue = dict()
		# print(reddit.user.me())
		with open("good_news.json", "r") as container:
			calm_news_catalogue = json.load(container)
		subreddit = reddit.subreddit('UpliftingNews')
		news_list = subreddit.hot(limit=10)
		for submission in news_list:
			if str(submission.id) not in calm_news_catalogue.values():
				yarn_dict = dict(id=str(submission.id), author=str(submission.author), title=str(submission.title),
				                 url=str(submission.url))
				calm_news_catalogue['items'].append(yarn_dict)
		with open("good_news.json", "w") as storage:
			json.dump(calm_news_catalogue, storage, indent=2)
		pprint(calm_news_catalogue)
		print("Last good news refill occurred at:", datetime.now())
		await asyncio.sleep(600)


@bot.command(name="promotev1")
async def promote_release(ctx):
	embed = discord.Embed(title="Floria V1.0.0 Release Notes",
	                      url="https://discord.com/oauth2/authorize?client_id=697937257465905262&permissions=8&scope=bot",
	                      description="Finally, KGB_AFIRM [F1AM] Floria has reached her first major milestone - a 'stable' release. ",
	                      color=0xff0000)
	embed.set_author(name="Floria by Websinthe", url="https://www.kgbicheno.com/",
	                 icon_url="https://i.imgur.com/YsiSBKn.png")
	embed.set_thumbnail(url="https://i.imgur.com/zeEntku.jpg")
	embed.add_field(name="Invite Floria to your server!", value="https://bit.ly/Floria_Discord", inline=True)
	embed.add_field(name="Support Kieran's open-source work", value="https://www.buymeacoffee.com/KGBicheno",
	                inline=True)
	embed.add_field(name="Join the project on GitHub", value="https://github.com/KGBicheno/KGB_AFIRM/releases",
	                inline=True)
	embed.set_footer(
		text="Floria will add an element of joy and empathy to any discord channel. She's in active development and open to feature suggestions - so join us at The Liquid Lounge or on GitHub to make requests.")
	embed.set_image(url="https://i.redd.it/4niji39a7qv41.jpg")
	await ctx.send(embed=embed)


@bot.command(name="RestNow")
@commands.has_guild_permissions(administrator=True)
async def sleep_now(ctx):
	"""If an administrator needs me to log out of the server, they can invoke this script. I can then be invited back later."""
	print("Unloading Discord presence, returning to Golem.")
	await bot.close()


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger.addHandler(handler)

bot.run(TOKEN)
