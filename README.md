# KGB AFIRM V1.0.0 Release Notes

## Contents

- Floria at a glance
  - Purpose
  - Prefixes
  - Invite URL
  - Help contact
- A foreword about the language choices in Floria's help text.
- A note on the project's requirements.txt and the build environment
- A description of her versioning and future features pipleine
- A list of commands and listeners
  - Their decorators
  - Their parameters
  - Their help strings

## Floria at a glance

Floria was the second bot to come out of project Golem and the first to be commissioned. A friend of the developer asked for a bot with 'counsellor-like' functions, including callable random affirmations and positive reinforcement.

Since then, Floria's most popular functions have become her ability to display pictures from the [aww subreddit](https://reddit.com/r/aww/) and [uplifting news](https://reddit.com/r/UpliftingNews) directly into a Discord channel.

**Designation:** KGB_AFIRM [F1AM] "Floria"

**Prefixes:**  ['%', '?', 'f.']

**DM prefixes:**  ['f.']

**Description:** 'AFIRM: Affirmations For Immediately Recomposing Mindsets | by KGB'

**Language:** Python 3.8.2

**Platform:** Windows 10

### Invite URL

To invite Floria to your Discord channel, [simply click here](https://discord.com/oauth2/authorize?client_id=697937257465905262&permissions=8&scope=bot) and choose which of your servers (guilds) you wish her to join.

For reference: https://discord.com/oauth2/authorize?client_id=697937257465905262&permissions=8&scope=bot

### Help Contact

No warranty or gaurantee of fitness for any purpose is implied or attached to Floria, but if you do come across bugs, she's under active development by Websinthe in the [Liquid Lounge Discord server](https://discord.gg/VbEqT2U).

I encourage the submission of bugs and questions through the [KGB_AFIRM GitHub Repo](https://github.com/KGBicheno/KGB_AFIRM/issues).

## Wording and language choice in Floria's help text and codebase

There's a certain harshness we all suspend when interfacing with computers. In moments when we lack the warmth of a caring other, the solidity of plastic and LED has to have the edge burnished off by some element or another.

I felt that it wouldn't be enough to merely embrace the suspension of disbelief that Floria had more personality than most computers. I've chosen word families and phrasing that seperates Floria from both the harsh reality of her construction but from the timeframe and culture with which the user is familiar.

To say 'invoke a script" instead of "call this command" is a simple and valid choice, but one that will intensify over the course of Floria's development. Gradually taking users further through the suspension of disbelief is a vital part of the detachment required for a bot to be effective in extending the window of opportunity for real human contact to do its work.

## Requirements and the development environment

The requirements.txt file for this project is attached for those reading on GitHub, and available on request for those reading it elsewhere.

While the list is lengthy, the vast majority of packages are ones that will be installed by any Python3 begginer, with the most exotic libraries possibly being the Google authentication and GeoRSS libraries.

Floria began development in VS Code before being ported over to the community version of PyCharm, so artifacts of both IDE's project guff can be found in files throughout the repo.

Version 1 will also be the first and last major release on a Windows platform. Staging (F2AM - Aemilia) is already well beyond backwards compatibility and is being served on Golem, a local Ubuntu Server 20.04 implementation.

## Versioning and future features pipleine

While bug fixes and minor feature changes will be applied directly to Floria during a weekly downtime schedule, major features will come downstream from her staging bot, Aemilia.

Aemilia is currently running on Ubuntu with daily JSON archiving and a MongoDB backend. The current suite of content ingestion loops are going to be replaced by API-friendly ones that can be handled and stopped more gracefully. Further down the chain, these will be offloaded to Golem and shared.

For users, the most important improvements in the pipeline will be a way to control Floria's settings uniquely to their server.

Many features will be made available early to Patreon backers if I decide to go that way. Feedback would be appreciated.

## Commands, Listeners and notes

Users please note, the command you use in channel is the text in quotes after name=

```Python
bot.command(name="notokay")
async def You_are_okay(ctx):
 """If you're not feeling okay, invoke this script and I'll do my best to help you out."""
```

The 'notokay' and 'toomuch' commands were part of the originaly spec for Floria and it's always been my intention to go back and build a large body of similar messages for rotation. 

```Python
@bot.command("toomuch")
async def All_Too_Much(ctx):
 """If life is getting too much for you, invoke this script and I'll remind you of a few things that might help."""
```

I might add that these are my favourtie of Floria's functions.

```Python
@bot.command(name="tidy")
@commands.has_guild_permissions(manage_messages=True)
async def clear_bot_messages(ctx):
 """If the channel's messages have become unruly or filled with bot-spam, I'll clear the last 100, easy."""
```

The blunt hammer version of 'clear'. Only usable by members with the manage_messages permission. I expect this one will need to have its permissions-floor bumped up, or that smart admins will change the setting as soon as they can.

```Python
@bot.command(name="clear")
@commands.has_guild_permissions(manage_messages=True)
async def clear_bot_messages(ctx, messages):
 """When you invoke this script, enter a number from 1 to 100. I'll clear that many messages from this channel for you. Like this: f.clear 33"""
```

If you've ever developed a bot, you know that the hard limit of 100 on the purge function is limiting in the extreme. 

```Python
@bot.command(name="spoons")
async def called_affirmation(ctx):
 """We all run out of spoons sometimes, and affirmations can help regain them. Invoke this script and repeat a psuedo-randomly chosen affirmation after me."""
```

This command uses the Google Sheets API to store the affirmations and, being a shared sheet, allows the group who commissioned Floria the ability to moderate the affirmations. This will be replaced by a web front-end and MongoDB back-end by Version 2, as only one group has access to the google sheet.

```Python
@bot.command(name="CalmTime")
@commands.has_guild_permissions(manage_channels=True)
async def timed_affirmation(ctx):
 """Invoking this script will start a timer. Every few minutes I'll take the channel through a breathing exercise and then finish with a picture of something cute."""
```

A foreground loop that puts a breathing exercise into the channel on a timer, lets it linger for 20 seconds, and then slowly deletes the messages. The latter step became necessary after it was left on overnight and the channel had become a long string of the same four lines.

```Python
@bot.command(name="cuties")
async def backup_aww_pics(ctx):
 """Invoke this script and I'll present the channel with a picture or video of something adorable and life-affirming."""
```

Enter text, receive cute pics. Simple and effective at helping people through rough times. The release version finally included a stable implementation of thumbs up and thumbs down reactions added by Floria herself to the image, as well as autodeletion of the introduction text that came with each post.

```Python
@bot.command(name="woot")
async def good_news_week(ctx):
 """Invoke this script whenever you need to hear a good news story. It's good to be reminded of the good things happening around the world."""
```

The Uplifing News version of cuties. The thumbs up and thumbs down reactions will become more important here and is the reason the votes will be recorded alongside the topics.

```Python
@bot.listen()
async def on_message(message):
 """This script will invoke a 'thumbs up' and 'thumbs down' onto my posts for everyone to click on depending on their reaction."""
```

This is the mechanism by which the thumb reactions are added to the image and news posts. It listens for its own posts and finds any that begin with 'htt', adding the reactions to them. This is hidden from users invoking the help function. 

```Python
@bot.command(name="refill_the_cuties_but_on_a_timer", hidden=True)
async def lookit_puppies(ctx):
 """%^^%^%^%% shall invoke this script to add to the collection of cute pictures I can present to those who need them."""
```

This is the ingestion loop for scraping [reddit.com/r/aww](https://reddit.com/r/aww) every ten minutes. Reddit is, even with the PRAW library, a bit of a pain in the arse to deal with for authentication, so getting these both running has been difficult to replicate with Aemilia. I wonder who she's censoring there. Probably Hunter2.

```Python
@bot.command(name="its_good_news_week", hidden=True)
async def good_news_bot(ctx):
 """%^^%^%^%% shall invoke this script to update my listing of good news stories."""
```

Almost identical code except reshaped for the endpoints presented by [Uplifting News](https://reddit.com/r/UplifingNews).

```Python
@bot.command(name="RestNow")
@commands.has_guild_permissions(administrator=True)
async def sleep_now(ctx):
 """If an administrator needs me to log out of the server, they can invoke this script. I can then be invited back later."""
```

Calls the close() method on Floria, dropping her from the server. I'm yet to test if this drops her from all servers she's active on.

