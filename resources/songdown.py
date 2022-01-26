# This is where the class that is used to download the songs is stored

import yt_dlp
import discord
import functools
from discord.ext import commands
import asyncio


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class Song(discord.PCMVolumeTransformer):

    YTDL_OPTIONS = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": False,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
    }

    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.uploader = data.get("uploader")
        self.uploader_url = data.get("uploader_url")
        date = data.get("upload_date")
        self.upload_date = date[6:8] + "." + date[4:6] + "." + date[0:4]
        self.title = data.get("title")
        self.thumbnail = data.get("thumbnail")
        self.description = data.get("description")
        self.tags = data.get("tags")
        self.url = data.get("webpage_url")
        self.views = data.get("view_count")
        self.likes = data.get("like_count")
        self.dislikes = data.get("dislike_count")
        self.stream_url = data.get("url")

    @classmethod
    async def create_data(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        print(search)
        if search.find("https://") != -1:
            partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
            data = await loop.run_in_executor(None, partial)

            if data is None:
                return False

            if "entries" not in data:
                process_info = data
            else:
                process_info = None
                for entry in data["entries"]:
                    if entry:
                        process_info = entry
                        break

                if process_info is None:
                    return False

            webpage_url = process_info["webpage_url"]
        else:
            webpage_url = search
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)
        playlist = False

        if processed_info is None:
            return False

        if "entries" not in processed_info:
            info = processed_info
        else:
            info = []
            playlist = True
            for entry in processed_info["entries"]:
                info.append(entry)

        if playlist:
            return_list = []
            for playlist_obj in info:
                return_list.append(cls(ctx, discord.FFmpegPCMAudio(playlist_obj["url"], **cls.FFMPEG_OPTIONS), data=playlist_obj))
            return return_list
        else:
            return cls(ctx, discord.FFmpegPCMAudio(info["url"], **cls.FFMPEG_OPTIONS), data=info)

