import os
import glob
import asyncio
import discord
import yt_dlp
from discord.ext import commands
from dotenv import load_dotenv
from config import *
import random
from queue_manager import local_queue

load_dotenv()
lq = local_queue()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''test description'''

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def e(ctx, password):
    if password == '1':
        exit(1)
        

@bot.command(aliases=['q'])
async def queue(ctx):
    queue = lq.get_songs_queue()
    if queue:
        _iter = 1
        for song in queue:
            if _iter == 1:
                embed = discord.Embed()
                embed.description = "This country is not supported, you can ask me to add it [here](your_link_goes_here)."
                await ctx.send(f'Current song is - {song["song_name"]}')
            else:
                await ctx.send(f'Song #{_iter} - {song["song_name"]}')
            _iter += 1
    else: 
        await ctx.send('Queue is empty')


@bot.command(aliases=['p', 'з'])
async def play(ctx, url=DEFAULT_SONG, loop=False):
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

    if ctx.voice_client.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, i will add your song in common queue')
        lq.add_song("song_name", url)

    else:

        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M','options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio/best', 'outtmpl': 'audios/%(extractor)s-%(id)s-%(title)s.%(ext)s','quiet': True, 'postprocessors': [{ 'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}
        
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)
            song_url = info['url']
            print(song_url)
            source = discord.FFmpegPCMAudio(source=song_url, options=FFMPEG_OPTIONS)
            vc = ctx.voice_client
            lq.add_song("song_name", url)
            vc.play(source)
            
            while vc.is_playing():
                await asyncio.sleep(1)
            if not vc.is_paused():
                if not loop:
                    lq.delete_song()   
                while len(lq.get_songs_queue()) != 0:
                    song_url = lq.get_songs_queue()[0]['song_name']
                    if not loop:
                        lq.delete_song()             
                    await play(ctx, song_url)
                await asyncio.sleep(300)
                await clean(ctx)
                await vc.disconnect()


@bot.command(aliases=['здфнд', 'pl', 'зд'])
async def playl(ctx, url=DEFAULT_SONG):
    await play(ctx, url, True)
            

@bot.command(aliases=['c', 'с'])
async def clean(ctx):
    pattern = "audios/*"
    files = glob.glob(pattern)
    for file in files:
        os.remove(file)


@bot.command(aliases=['n'])
async def next(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()


@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()


@bot.command(aliases=['d', 'в'])
async def drop(ctx):
    lq.pune_queue() 
    await ctx.voice_client.disconnect()


@bot.command()
async def join(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        return
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


bot.run(os.getenv('TOKEN'))
