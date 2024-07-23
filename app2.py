import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import *
import random
from queue_manager import local_queue
from youtube_dl import YoutubeDL
import yt_dlp

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
        

@bot.command()
async def cc(ctx):
    await ctx.send('p!play Never Gonna Give You Up')


@bot.command(aliases=['t'])
async def tinkoff(ctx, phrase_number=0):
    if not phrase_number:
        phrase_number = random.randint(1, 115)
        await local_play(ctx, f'audios/{phrase_number}.mp3')
    else:
        await local_play(ctx, f'audios/{phrase_number}.mp3')


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
async def rick(ctx):
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

    if ctx.voice_client.is_playing():
        await ctx.send("something is currently playing...")
        return

    FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
        'options': '-vn'
    }
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        secret = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        info = ydl.extract_info(secret, download=False)
        url2 = info['url']
        print(url2)
        source = discord.FFmpegPCMAudio(url2)
        vc = ctx.voice_client
        vc.play(source)


# @bot.command(aliases=['здфнд', 'pl', 'зд'])
# async def playl(ctx, url=DEFAULT_SONG):
#     await play(ctx, url, True)
            

# @bot.command()
# async def local_play(ctx, path_to_song):
#     await join(ctx)

#     guild = ctx.message.guild
#     voice_client = guild.voice_client
#     voice_client.play(
#         discord.FFmpegPCMAudio(path_to_song)
#     )
#     voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

#     while voice_client.is_playing():
#         await asyncio.sleep(1)
#     else:
#         await asyncio.sleep(15)
#         while voice_client.is_playing():
#             break
#         else:
#             await voice_client.disconnect()


@bot.command(aliases=['c', 'с'])
async def cycle(ctx):

    await ctx.voice_client.disconnect()


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
