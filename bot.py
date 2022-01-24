import discord

bot = discord.Bot()

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

