import discord
import json

bot = discord.Bot()

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
    ctx.reply(embed=discord.Embed(title=message, color=config_theme))


# Bot commands

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config_status))

    print("Rytem is online!\n\nBot Name: " + bot.user.name + "\nBot ID: " + str(bot.user.id) + "\n\nIn servers:")
    for guild in bot.guilds:
        print(str(guild.name))


@bot.slash_command()
async def play(ctx):

    # Variables
    author = ctx.author
    bot_vc = ctx.voice_client.channel
    author_vc = author.voice


@bot.slash_command()
async def skip(ctx):
    pass


@bot.slash_command()
async def leave(ctx):
    pass


@bot.slash_command()
async def forceskip(ctx):
    pass


@bot.slash_command()
async def top(ctx):
    pass


# Bot running stuff

bot.run(config_token)

