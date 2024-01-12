import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!',
                   description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def r(ctx, phrase_number=0):
    if not phrase_number:
        phrase_number = random.randint(1, 115)
        await play(ctx, f'audios/{phrase_number}.mp3')
    else:
        await play(ctx, f'audios/{phrase_number}.mp3')


@bot.command()
async def play(ctx, path_to_song):
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
        await asyncio.sleep(120)
        while voice_client.is_playing():
            break
        else:
            await voice_client.disconnect()


@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()


@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()


# TODO
# @bot.command()
# async def next(ctx):
#     pass


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
