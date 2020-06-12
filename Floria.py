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
from urllib.request import urlopen
import random
from discord.client import Client
import urllib.request
from bs4 import BeautifulSoup

#TODO f.help | Override Floria's help class to have it present more clearly and professionaly


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/websinthe/sambashare/KGB_Golem/KGB_AFIRM/Credentials.json",
                                                               scope)
#TODO ||Google block|| Completely remove my use of Google Sheets from Floria.
gclient = gspread.authorize(credentials)
AFFIRM_SOURCE = gclient.open("Affirmations")
affirm_list = AFFIRM_SOURCE.get_worksheet(0)

#TODO get_prefix() Put more thought into how you're advertising Floria's functions to new users
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

#TODO ||getenv block|| make sure the test unit isn't compromising the use of these at all
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
NASA_API_KEY = os.getenv('NASA_API_KEY')
client = discord.Client

#TODO on_ready() Have this integrate with bot_conf and look into finally implementing cogs
@bot.event
async def on_ready():
	purpose = discord.Game(
		"%Help for responses | I'm here if you need me, either in chat or by DM. Either is fine by me :D.")
	await bot.change_presence(activity=purpose)
	print(f'{bot.user.name} is connected to Discord!')

#TODO on_member_join() Hook this up to bot_conf when it gets pulled over and test it until it works
@bot.event
async def on_member_join(ctx, member):
	if member.name != bot.user.name:
		await ctx.send("It's wonderful to have you along, " + member.name)
	elif member.name == "Brook Newsly":
		await ctx.send("I feel much safer now that you're here, sister. Welcome back, Brook.")
	else:
		await ctx.send("What a lovely place to place to be.")

#TODO You_are_okay() This is one of my favourite functions - write at least 50 more and pull them in from a JSON file
@bot.command(name="notokay")
async def You_are_okay(ctx):
	"""If you're not feeling okay, invoke this script and I'll do my best to help you out."""
	friend = ctx.author.id
	await ctx.send("Hey, <@" + str(
		friend) + ">, you're okay. You're more than okay. You've just temporarily lost sight of how complex and unique you are. You're okay.")

#TODO All_too_much() I love this function - write at least 50 or so and pull them from a JSON file
@bot.command("toomuch")
async def All_Too_Much(ctx):
	"""If life is getting too much for you, invoke this script and I'll remind you of a few things that might help."""
	friend = ctx.author.id
	await ctx.send("It sounds like something's gotten you snowed under, hey <@" + str(
		friend) + ">? Just remember, you've probably felt this way before and lived to tell the tale. I hope one day I learn how to understand what you've been through and survived. It sounds like you've got what it takes to surprise yourself.")

#TODO clear_messages() Test this function until it works
@bot.command(name="tidy")
@commands.has_guild_permissions(manage_messages=True)
async def clear_messages(ctx):
	"""If the channel's messages have become unruly or filled with bot-spam, I'll clear the last 100, easy."""
	await channel.TextChannel.purge(ctx, limit=100, check=None, bulk=True)
	print("messages deleted")

#TODO clear_bot_messages() Test this function until it works
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

#TODO called_affirmations() Overhaul this function to run off a JSON file instead of Google Sheets
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

#TODO timed_affirmations() overhaul this function to include a larger array of breathing excercises and run off JSON instead of GS
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


#TODO backup_aww_pics() include optional arguments for type of media to return 
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


#TODO Add a counter and give percistance to the upvote/downcote symbols on each post
@bot.command(name="cutebots")
async def cutebots(ctx):
	"""This script summons cute bots!"""
	url = "https://cutebotcalendar.tumblr.com/"
	parsed_url = urlopen(url)
	bot_page = parsed_url.read()
	soup = BeautifulSoup(bot_page, 'html.parser')
	photo_list = []
	date_list = []
	for post in soup.find_all("div", "date"):
		print(post.text.strip())
		post_date = post.text.strip()
		date_list.append(post_date)
	for image in soup.find_all("img", "photo"):
		print(image.get('src'))
		post_image = image.get('src')
		photo_list.append(post_image)
	index = range(len(photo_list))
	for x in index:
		print(date_list[x])
		print(photo_list[x])
	await ctx.send("Today's cutebotcalendar presents:")
	await ctx.send(date_list[0])
	await ctx.send(photo_list[0])


#TODO good_news_week() Add a trigger warning setting to bot_conf to filter this function's output
# Also find a way of checking if they're actually uplifting, possibly by upvotes. Too many failures have come through.
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

#TODO on_message() Find a way to have this activate on any embed-type message the bot sends
@bot.listen()
async def on_message(message):
	if message.author.id == bot.user.id:
		target = message.content
		if target[:3] == "htt":
			await message.add_reaction('\U0001f44d')
			await message.add_reaction('\U0001F44E')

#TODO woah() Check the endpoint for description data to make the images searchable by topic and add an optional parameter
@bot.command(name="woah")
async def nasa_apod(ctx):
	"""Invoke this script to cast your eyes across the universe to behold its wonders. What are our problems compared to such majesty? We are part of something staggering. """
	url = "https://api.nasa.gov/planetary/apod"
	await ctx.send("aligning mirrors")
	year = str(random.randint(1996, 2020))
	print(year)
	month = str(random.randint(1, 12)).zfill(2)
	print(month)
	day = str(random.randint(1, 28)).zfill(2)
	print(day)
	date = year + "-" + month + "-" + day
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
	embed.set_footer(text="One day, with shuffling steps, we will get there.")
	await ctx.send(embed=embed)

#TODO nasa_mars() Look into optional arguments to have the L/R photos joined horizontally or show different cameras
@bot.command(name="mars")
async def nasa_mars(ctx):
	"""Invoke this script to scry the lands of the planet Mars through the eyes of the intrepid explorer, and my hero, Curiosity. """
	url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
	await ctx.send("Establishing interplanetary connection ...", delete_after=50)
	await asyncio.sleep(2)
	await ctx.send("Spooling up FTL signal modulator ...", delete_after=50)
	await asyncio.sleep(2)
	await ctx.send("Attempting Entanglement Twin Transfer Protocol ... ", delete_after=50)
	sol = random.randint(1, 2778)
	camera = "FHAZ"
	api_key = NASA_API_KEY
	await asyncio.sleep(2)
	await ctx.send("Sending request to ettp://sol.curiosity.mars/ ...", delete_after=50)
	PARAMS = {'sol':sol, 'camera':camera, 'api_key':api_key}
	r = requests.get(url=url, params=PARAMS)
	album = r.json()
	await asyncio.sleep(3)
	await ctx.send("Response detected!", delete_after=50)
	left_camera = album.get("photos")[0]
	right_camera = album.get("photos")[1]
	sol = left_camera.get("sol")
	earth_date = left_camera.get("earth_date")
	left_image = left_camera.get("img_src")
	right_image = right_camera.get("img_src")
	description = "Rover: Curiosity \n Sol {} \n Earth date: {} \n Two photos recieved, left-hand & right-hand forward hazard cameras.".format(sol, earth_date)
	await ctx.send(description)
	await ctx.send(left_image)
	await ctx.send(right_image)

#TODO no_borders() Pull down all the images for a date and find a library to convert them into a slow gif
@bot.command(name="noborders")
async def no_borders(ctx):
	url = "https://api.nasa.gov/EPIC/api/enhanced/images?api_key={}".format(NASA_API_KEY)
	payload = {}
	headers = {
		'Cookie': 'XSRF-TOKEN=eyJpdiI6IjhHUjdidjVKVGNoOGlWTXRyZjNNSFE9PSIsInZhbHVlIjoiXC91ZlpwbURjY1RRXC9RU2tvQVNtaWxydVA4akxNcEtZVVZwMVBidDJuSDhQT1Y0bG1KRU8zV3l6ZlZDTFB6RVhoIiwibWFjIjoiMjdkNGNhNjZkZWU1NGRkZTY4OTZkM2Y5YTRmMGZmMThkNTgxMGE5Y2U2MmRkYjQyMmFlYWI1NDM2NTJmMWFlMiJ9; laravel_session=eyJpdiI6IkR3NjhpV0E3VU5TV3oyd1RGdm1wZ2c9PSIsInZhbHVlIjoiVkczazhvc1dmRGJOa0IrRlFHa1BadUsyVGVSOUpYUGJoeUpXdnYxTVpCZEQ0TTc5NlhFVmhlWjRyY0dvMGVxUiIsIm1hYyI6IjUzMzhhMjNmYzA5NzVmYmFlNTVhZTlmMmRjNzAwZmMxMGJlNWFmM2RjMGY5ZGJmNmU2YzUzN2JjNzZhN2Y2MDcifQ%3D%3D'
	}

	response = requests.request("GET", url, headers=headers, data=payload)
	print(type(response))
	for x in response.json():
		photo_description = str(x.get("caption"))
		photo_slug = str(x.get("image"))
		photo_time = (str(x.get("date"))).split(" ", 1)
		photo_date = photo_time[0]
		print(photo_date)
		photo_year = photo_date[0:4]
		photo_month = photo_date[5:7].zfill(2)
		photo_day = photo_date[8:10].zfill(2)
		photothumb = "https://epic.gsfc.nasa.gov/archive/enhanced/{}/{}/{}/thumbs/{}.jpg".format(photo_year,
																									photo_month,
																									photo_day,
																									photo_slug)
		photo_url = "https://epic.gsfc.nasa.gov/archive/enhanced/{}/{}/{}/png/{}.png".format(photo_year,
																								photo_month, photo_day,
																								photo_slug)
	print(photo_url)
	await ctx.send("Incoming transmission from the L1 Lagrange point. \n NASA::EPIC light-codex captured. \n Scrying truth from the void ...")
	embed = discord.Embed(title="There are no borders",
							url=photo_url,
							description=photo_description,
							color=0xffffff)
	embed.set_author(name="NASA EPIC", icon_url="https://i.imgur.com/7gnuJ1z.png")
	embed.set_thumbnail(url=photothumb)
	embed.set_image(url=photo_url)
	embed.set_footer(
		text="It's not enough to remember there are no borders. One has to remember how much of your daily lives are contrived. Base principles are forgotten. Harmony is imperitive.")
	await ctx.send(embed=embed)

#TODO lookit_puppies() Reinvestigate the endpoint for future analytical needs
@bot.command(name="refill_the_cuties", hidden=True)
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

#TODO good_news_bot() Map the reddit endpoint for future analytical needs
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


@bot.command(name="support")
async def support_line(ctx):
	"""Support lines for mental health situations as needed. Please feel free to use them. """
	embed=discord.Embed(title="Suicide Call Back Service", url="https://www.suicidecallbackservice.org.au/", description="Suicide Call Back Service provides 24/7 support if you or someone you know is feeling suicidal.", color=0xffffff)
	embed.set_author(name="Mental Health Help Line", url="https://www.suicidecallbackservice.org.au/", icon_url="https://i.imgur.com/xfocDnV.png")
	embed.set_thumbnail(url="https://i.imgur.com/xfocDnV.png")
	embed.add_field(name="Phone", value="1300 659 467", inline=False)
	embed.set_footer(text="Open 24/7")
	await ctx.send(embed=embed)
    
	embed9=discord.Embed(title="QLife", url="https://qlife.org.au/", description="QLife provides nationwide telephone and web-based services to support lesbian, gay, bisexual, transgender and intersex (LGBTI) people of all ages.", color=0xffffff)
	embed9.set_author(name="Mental Health Help Line", url="https://qlife.org.au/", icon_url="https://i.imgur.com/huk43uW.png")
	embed9.set_thumbnail(url="https://i.imgur.com/huk43uW.png")
	embed9.add_field(name="Phone", value="1800 184 527", inline=False)
	embed9.set_footer(text="3pm-12am (midnight) AEST / 7 days a week")
	await ctx.send(embed=embed9)

	embed3=discord.Embed(title="Butterfly Foundation's National Helpline", url="https://thebutterflyfoundation.org.au/our-services/helpline/over-the-phone/", description="ED HOPE, is a free, confidential service that provides information, counselling and treatment referral for people with eating disorders, and body image and related issues.", color=0xffffff)
	embed3.set_author(name="Mental Health Help Line", url="https://thebutterflyfoundation.org.au/our-services/helpline/over-the-phone/", icon_url="https://i.imgur.com/BYzgxVa.png")
	embed3.set_thumbnail(url="https://i.imgur.com/BYzgxVa.png")
	embed3.add_field(name="Phone", value="1800 650 890", inline=False)
	embed3.set_footer(text="8am-midnight AEST / 7 days a week")
	await ctx.send(embed=embed3)

	embed4=discord.Embed(title="eheadspace", url="https://headspace.org.au/eheadspace/", description="eheadspace provides mental health and wellbeing support, information and services to young people aged 12 to 25 years and their families.", color=0xffffff)
	embed4.set_author(name="Mental Health Help Line", url="https://headspace.org.au/eheadspace/", icon_url="https://i.imgur.com/NT1YKMc.png")
	embed4.set_thumbnail(url="https://i.imgur.com/NT1YKMc.png")
	embed4.add_field(name="Phone", value="1800 33 4673", inline=False)
	embed4.set_footer(text="8am-midnight AEST / 7 days a week")
	await ctx.send(embed=embed4)

	embed5=discord.Embed(title="Kids Help Line", url="https://kidshelpline.com.au/", description="Kids Helpline is Australiaâ€™s only free 24/7 confidential and private counseling service specifically for children and young people aged 5 to 25.", color=0xffffff)
	embed5.set_author(name="Mental Health Help Line", url="https://kidshelpline.com.au/", icon_url="https://i.imgur.com/mnvvDRQ.png")
	embed5.set_thumbnail(url="https://i.imgur.com/mnvvDRQ.png")
	embed5.add_field(name="Phone", value="1800 55 1800", inline=False)
	embed5.set_footer(text="Open 24/7 ")
	await ctx.send(embed=embed5)

	embed6=discord.Embed(title="Lifeline", url="https://www.lifeline.org.au/", description="Lifeline provides 24-hour crisis counselling, support groups and suicide prevention services.", color=0xffffff)
	embed6.set_author(name="Mental Health Help Line", url="https://www.lifeline.org.au/", icon_url="https://i.imgur.com/84dYdDv.png")
	embed6.set_thumbnail(url="https://i.imgur.com/84dYdDv.png")
	embed6.add_field(name="Phone", value="13 11 14.", inline=False)
	embed6.set_footer(text="Open 24/7")
	await ctx.send(embed=embed6)

	embed7=discord.Embed(title="MensLine Australia", url="https://mensline.org.au/", description="MensLine Australia is a professional telephone and online support and information service for Australian men.", color=0xffffff)
	embed7.set_author(name="Mental Health Help Line", url="https://mensline.org.au/", icon_url="https://i.imgur.com/ldayfoE.png")
	embed7.set_thumbnail(url="https://i.imgur.com/ldayfoE.png")
	embed7.add_field(name="Phone", value="1300 78 99 78", inline=False)
	embed7.set_footer(text="Open 24 hours / 7 days a week")
	await ctx.send(embed=embed7)

	embed8=discord.Embed(title="MindSpot", url="https://mindspot.org.au/", description="MindSpot is a free telephone and online service for people with stress, worry, anxiety, low mood or depression. It provides online assessment and treatment for anxiety and depression. MindSpot is not an emergency or instant response service.", color=0xffffff)
	embed8.set_author(name="Mental Health Help Line", url="https://mindspot.org.au/", icon_url="https://i.imgur.com/G8Cz800.png")
	embed8.set_thumbnail(url="https://i.imgur.com/G8Cz800.png")
	embed8.add_field(name="Phone", value="1800 61 44 34", inline=False)
	embed8.set_footer(text="AEST, 8am-8pm (Mon-Fri), 8am-6pm (Sat)")
	await ctx.send(embed=embed8)


##TODO promote_release() See if it's possible to have a subtle gif or a rotating image replace the current image embed
#@bot.command(name="me")
#async def promote_release(ctx):
#	embed = discord.Embed(title="Hi I'm Floria!",
#	                      url="https://discord.com/oauth2/authorize?client_id=697937257465905262&permissions=8&scope=bot",
#	                      description="I'm part of a team developed to try help when things aren't going so well. To explain, I was first created during the pandemic to help keep people company during isolation. Now I do the best I can to remind people that the world can be a wonderful place, even when life throws its worst at you.\n Try invoking my scripts like f.cuties, f.woah, or f.woot.\n See f.help for the full list!",
#	                      color=0xff0000)
#	embed.set_author(name="Floria by KGBicheno", url="https://www.kgbicheno.com/",
#	                 icon_url="https://i.imgur.com/YsiSBKn.png")
#	embed.set_thumbnail(url="https://i.imgur.com/zeEntku.jpg")
#	embed.add_field(name="Invite Floria to your server!", value="https://bit.ly/Floria_Discord", inline=False)
#	embed.add_field(name="Support Kieran's community work", value="https://www.buymeacoffee.com/KGBicheno",
#	                inline=False)
#	embed.add_field(name="Join us on Patreon for tutorials and experimental features", value="https://www.patreon.com/KGBicheno",
#	                inline=False)
#	embed.add_field(name="Join the project on GitHub", value="https://github.com/KGBicheno/KGB_AFIRM/",
#	                inline=False)
#	embed.set_footer(
#		text="Floria will add an element of joy and empathy to any discord channel. She's in active development and open to feature suggestions - so join us at The Liquid Lounge or on GitHub to make requests.")
#	embed.set_image(url="https://i.imgur.com/6Ckhy5I.png")
#	await ctx.send(embed=embed)

@bot.command(name="SitRep", hidden=True)
@commands.is_owner()
async def guild_spread(ctx):
	await ctx.author.create_dm()
	await ctx.author.send("I believe you were looking for this, yes? It's a list of all the guilds who've enlisted my talents.")
	coverage = bot.guilds
	for server in coverage:
		await ctx.author.create_dm()
		await ctx.author.send(server)

#TODO maint_list() Have the results of the server sweep piped into bot_conf once pulled over from the test unit
@bot.command(name="maint_list", hidden=True)
@commands.is_owner()
async def maint_list(ctx):
	broadcast = []
	patch = bot.guilds
	for server in patch:
		for chat in server.text_channels:
			broadcast.append([server.name, chat.name, chat.id])
	await ctx.send("I've made a list of the places my voice can be heard. Their numerals can be used to connect with those who dwell there.")
	for x in range(len(broadcast)):
		server_name = broadcast[x][0]
		text_chat_name = broadcast[x][1]
		text_chat_id = broadcast[x][2]
		text_details = "Name: {} \n Id: {}".format(text_chat_name, text_chat_id)
		await ctx.send(server_name)
		await ctx.send(text_details)

#TODO maint_mode() Implement Maint_mode to signal to servers or their owners that Floria will be entering maintainance mode and going offline

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
