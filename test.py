import os
import glob
import asyncio
import discord
import yt_dlp
from discord.ext import commands
from dotenv import load_dotenv
from config import *
import random

FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M','options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best', 'cookiesfrombrowser': ('chrome',), 'verbose': True, 'outtmpl': 'audios/%(extractor)s-%(id)s-%(title)s.%(ext)s','quiet': True, 'postprocessors': [{ 'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}
url = "https://www.youtube.com/watch?v=VtjiCRzKEDA"

with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:

    print('00000000000000')

    info = ydl.extract_info(url, download=True)
    song_url = info['url']

    print('11111111111111')