# This file is used to create embeds for the song queue

import discord
from resources import emojis
import datetime
import json

with open("config.json") as file:
    json = json.loads(file.read())
    raw_color = json["bot_settings"]["color_theme_rgb"].split(", ")
    config_theme = discord.Color.from_rgb(int(raw_color[0]), int(raw_color[1]), int(raw_color[2]))

def now_playing(source):
    embed = discord.Embed()
    embed.title = emojis.play + " Now Playing"
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = source.title
    embed.set_footer("Requested by: " + source.requester.name, (source.requester.avatar_url))

def queued(source):
    embed = discord.Embed()
    embed.title = emojis.down_arrow + " Queued Song"
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = source.title
    embed.set_footer("Requested by: " + source.requester.name, (source.requester.avatar_url))