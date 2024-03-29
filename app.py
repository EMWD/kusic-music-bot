import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import *
import random
from queue_manager import local_queue
from youtube_dl import YoutubeDL

load_dotenv()
lq = local_queue()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''test description'''

bot = commands.Bot(command_prefix='!',
                   description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def e(ctx, password):
    if password == '1':
        exit(1)


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


@bot.command(aliases=['здфн', 'з', 'p'])
async def play(ctx, url=DEFAULT_SONG, loop=False):
    

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    global vc
    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except discord.ClientException as ce:
        pass

    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, i will add your song in common queue')
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        song_name = 'song_name'
        lq.add_song(song_name, url)
    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url'] 
        song_name = 'song_name'
        lq.add_song(song_name, url)
        vc.play(discord.FFmpegPCMAudio(source = URL, **FFMPEG_OPTIONS))
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
            await vc.disconnect()


@bot.command(aliases=['здфнд', 'pl', 'зд'])
async def playl(ctx, url=DEFAULT_SONG):
    await play(ctx, url, True)
            

@bot.command()
async def local_play(ctx, path_to_song):
    await join(ctx)

    guild = ctx.message.guild
    voice_client = guild.voice_client
    voice_client.play(
        discord.FFmpegPCMAudio(path_to_song)
    )
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    while voice_client.is_playing():
        await asyncio.sleep(1)
    else:
        await asyncio.sleep(15)
        while voice_client.is_playing():
            break
        else:
            await voice_client.disconnect()


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
