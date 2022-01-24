import discord
import json

import emojis
import queues
from discord.ext import commands

bot = discord.Bot()
queue = queues.Queue()

# Config parser

with open("config.json") as file:
    try:
        json = json.loads(file.read())
        config_token = json["bot_settings"]["token"]
        config_status = json["bot_settings"]["playing_status_message"]
        raw_color = json["bot_settings"]["color_theme_rgb"].split(", ")
        config_theme = discord.Color.from_rgb(int(raw_color[0]), int(raw_color[1]), int(raw_color[2]))
    except:
        print("\n[Config Parser] Config invalid")
        exit()


# Send message function

def send_message(ctx, message):
    a = ctx.respond(embed=discord.Embed(title=message, color=config_theme))
    return a


# Bot commands

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config_status))

    print("Rytem is online!\n\nBot Name: " + bot.user.name + "\nBot ID: " + str(bot.user.id) + "\n\nIn servers:")
    for guild in bot.guilds:
        print(str(guild.name))


@bot.slash_command()
async def play(ctx: commands.Context):

    if ctx.author.voice is None:
        await send_message(ctx, emojis.no + " You must be in a VC to use this command")


@bot.slash_command()
async def loop(ctx: commands.Context):
    queue.loop = not queue.loop
    if queue.loop:
        await send_message(ctx, emojis.loop + " Enabled")
    else:
        await send_message(ctx, emojis.loop + " Disabled")


@bot.slash_command()
async def skip(ctx: commands.Context):
    pass

@bot.slash_command()
async def leave(ctx: commands.Context):
    pass


@bot.slash_command()
async def forceskip(ctx: commands.Context):
    pass


@bot.slash_command()
async def top(ctx: commands.Context):
    pass


# Bot running stuff

bot.run(config_token)

