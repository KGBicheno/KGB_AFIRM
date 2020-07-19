import asyncio
import json
import logging
import os
import random
from datetime import date, datetime
from pprint import pprint
from urllib.request import urlopen
from discord.ext.commands import Context
import discord
import gspread
import praw
import requests
from bs4 import BeautifulSoup
from discord import channel
from discord.ext import commands
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

class CuteTimesCog(commands.Cog, name='Cute Times'):
	"""Sometimes the world outside must be viewed through the correct glass, made from sands so pure one can only
	see cute puppies, silly animals, and good news stories."""
	def __init__(self, bot):
		self.bot = bot
		self.reddit_secret = os.getenv('REDDIT_SECRET')
		self.refresh_token = os.getenv('REFRESH_TOKEN')
		self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')

	# TODO backup_aww_pics() include optional arguments for type of media to return
	@commands.command(name="cuties")
	async def backup_aww_pics(self, ctx: Context):
		"""Invoke this script and I'll present the channel with a picture or video of something adorable and
		life-affirming."""
		self.bot.logger.info(f"cuties has been invoked.")
		with open("/home/websinthe/code/KGB_AFIRM/calm_posts.json", "r") as source:
			pic_container = json.load(source)
		pic_list = pic_container["images"]
		pic_hit = random.randrange(1, len(pic_list))
		dict_pic = pic_list[pic_hit]
		v = dict_pic.get('url')
		await ctx.channel.send("Here's some cute! I hope it helps!", delete_after=20)
		await ctx.channel.send(v)

	# TODO Add a counter and give percistance to the upvote/downcote symbols on each post
	@commands.command(name="cutebots")
	async def cutebots(self, ctx: Context):
		"""This script summons cute bots!"""
		self.bot.logger.info(f"cutebots has been invoked.")
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

	# TODO good_news_week() Add a trigger warning setting to bot_conf to filter this function's output
	# Also find a way of checking if they're actually uplifting, possibly by upvotes. Too many failures have come
	# through.
	@commands.command(name="woot")
	async def good_news_week(self, ctx: Context):
		"""Invoke this script whenever you need to hear a good news story. It's good to be reminded of the good things
		happening around the world."""
		self.bot.logger.info(f"woot has been invoked.")
		with open("/home/websinthe/code/KGB_AFIRM/good_news.json", "r") as source:
			yarn_container = json.load(source)
		yarn_list = yarn_container["items"]
		yarn_hit = random.randrange(1, len(yarn_list))
		dict_yarn = yarn_list[yarn_hit]
		v = dict_yarn.get('url')
		await ctx.channel.send("Hopefully this reminds you that there's still good in the word!", delete_after=20)
		await ctx.channel.send(v)

	# TODO lookit_puppies() Reinvestigate the endpoint for future analytical needs
	@commands.command(name="refill_the_cuties", hidden=True)
	async def lookit_puppies(self, ctx: Context):
		"""%^^%^%^%% shall invoke this script to add to the collection of cute pictures I can present to those who
		need them."""
		self.bot.logger.info(f"cute images ingestion has begun.")
		while self.bot.is_ready():
			reddit = praw.Reddit(client_id=self.reddit_client_id,
			                     client_secret=self.reddit_secret,
			                     refresh_token=self.refresh_token,
			                     user_agent="Floria_bot by /u/websinthe")
			calm_posts_catalogue = dict()
			with open("/home/websinthe/code/KGB_AFIRM/calm_posts.json", "r") as container:
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
			with open("/home/websinthe/code/KGB_AFIRM/calm_posts.json", "w") as container:
				json.dump(calm_posts_catalogue, container, indent=2)
			pprint(calm_posts_catalogue)
			print("Last refill occurred at:", datetime.now())
			await asyncio.sleep(600)

	# TODO good_news_bot() Map the reddit endpoint for future analytical needs
	@commands.command(name="its_good_news_week", hidden=True)
	async def good_news_bot(self, ctx: Context):
		"""%^^%^%^%% shall invoke this script to update my listing of good news stories."""
		self.bot.logger.info(f"good news ingestion has begun.")
		while self.bot.is_ready():
			reddit = praw.Reddit(client_id=self.reddit_client_id,
			                     client_secret=self.reddit_secret,
			                     refresh_token=self.refresh_token,
			                     user_agent="Floria_bot by /u/websinthe")
			calm_news_catalogue = dict()
			# print(reddit.user.me())
			with open("/home/websinthe/code/KGB_AFIRM/good_news.json", "r") as container:
				calm_news_catalogue = json.load(container)
			subreddit = reddit.subreddit('UpliftingNews')
			news_list = subreddit.hot(limit=10)
			for submission in news_list:
				if str(submission.id) not in calm_news_catalogue.values():
					yarn_dict = dict(id=str(submission.id), author=str(submission.author), title=str(submission.title),
					                 url=str(submission.url))
					calm_news_catalogue['items'].append(yarn_dict)
			with open("/home/websinthe/code/KGB_AFIRM/good_news.json", "w") as storage:
				json.dump(calm_news_catalogue, storage, indent=2)
			pprint(calm_news_catalogue)
			print("Last good news refill occurred at:", datetime.now())
			await asyncio.sleep(600)


def setup(bot):
	"""
    Register this cog as an extension.
    """
	bot.add_cog(CuteTimesCog())