import discord
import json

bot = discord.Bot()

# Config parser

with open("config.json") as file:
    json = json.loads(file.read())
    config_token = json["bot_settings"]["token"]
    config_status = json["bot_settings"]["playing_status_message"]
    config_theme = json["bot_settings"]["color_theme_rgb"]

# Bot commands

@bot.event
async def on_ready():
    print("Rytem is online!\n\nBot Name: " + bot.user.name + "\nBot ID: " + str(bot.user.id) + "\n\nIn servers:")
    for guild in bot.guilds:
        print(str(guild.name))

@bot.slash_command()
async def play(ctx):

    # Variables
    author = ctx.author
    bot_vc = ctx.voice_client.channel

bot.run(config_token)

