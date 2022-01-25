import discord
import json

from resources import queues, emojis, songdown
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
class Music(commands.Cog):

    def __init__(self, dis_bot):
        self.bot = dis_bot

    @commands.slash_command(description="Plays a song")
    async def play(self, ctx: commands.Context, *, song):

        if ctx.author.voice is None:
            await send_message(ctx, emojis.no + " You must be in a VC to use this command")
        user_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await user_channel.connect()
        if user_channel != ctx.voice_client.channel:
            cur_channel_mem_count = len(ctx.voice_client.channel.members)
            if cur_channel_mem_count == 1:
                await user_channel.connect()
            else:
                if queue.now_playing is None:
                    await user_channel.connect()
                else:
                    send_message(ctx, emojis.no + " Someone else is using the bot right now")

        async with ctx.typing():
            source = await songdown.Song.create_data(ctx, song, loop=self.bot.loop)
            if not source:
                return send_message(ctx, emojis.no + " Can't find any results for: `" + song + "`")
            now_playing = queue.now_playing
            queue.add(source)

    @commands.slash_command(description="Toggles song looping")
    async def loop(self, ctx: commands.Context):
        queue.loop = not queue.loop
        if queue.loop:
            await send_message(ctx, emojis.loop + " Enabled")
        else:
            await send_message(ctx, emojis.loop + " Disabled")

    @commands.slash_command(description="Votes to skip the song")
    async def skip(self, ctx: commands.Context):
        pass

    @commands.slash_command(description="Makes the bot clear queue and leave the VC (DJ role required)")
    async def leave(self, ctx: commands.Context):
        pass

    @commands.slash_command(description="Forces the current song to skip (DJ role required)")
    async def forceskip(self, ctx: commands.Context):
        pass

    @commands.slash_command(description="Displays top listeners for specified artist (DJ role required)")
    async def topartist(self, ctx: commands.Context, *, artist):
        pass

    @commands.slash_command(description="Displays top listeners for specified song (DJ role required)")
    async def topsong(self, ctx: commands.Context, *, song):
        pass

    @commands.slash_command(description="Displays top listeners for specified album (DJ role required)")
    async def topalbum(self, ctx: commands.Context, *, album):
        pass


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config_status))

    print("Rytem is online!\n\nBot Name: " + bot.user.name + "\nBot ID: " + str(bot.user.id) + "\n\nIn servers:")
    for guild in bot.guilds:
        print(str(guild.name))

# Bot running stuff
bot.add_cog(Music(bot))
bot.run(config_token)

