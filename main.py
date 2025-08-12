import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
from asyncio import sleep

# load .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

sounds = {
    "ambatukam": "ambatukam.mp3",
    "leave": "discord-leave.mp3",
    "watesigma": "Erm, What the Sigma_ - Sound Effect.mp3",
    "wuatdehel" : "wewewew wutdaheeel.mp3",
    "wssk" : "wong saya suka kok #shorts #fyp #ganjar #memesdaily.mp3",
    "knock" : "y2mate.com - Knock knock sound effect (1).mp3",
    "omkegams" : "y2mate.com - OKE GAS PRABOWO GIBRAN PALING PAS.mp3"
}
sound_directory = "./soundboards"

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready")


@bot.command()
async def ping(ctx):
    await ctx.reply(f'Pong! {ctx.author.mention}')

@bot.command()
async def fuckyou(ctx, name = None):
    name = name if name else ctx.author.name
    url = "https://insult.mattbas.org/api/insult"
    params = {
        "lang": "en",
        "who": name
    }
    response = requests.get(url, params=params)
    await ctx.reply(response.text)
    
@bot.command()
async def sound(ctx, sound: str):
    if ctx.author.voice and ctx.author.voice.channel:
        print('Masuk voice channel')
        channel = ctx.author.voice.channel
        print (channel)
        try:
            if not ctx.voice_client:
                vc = await channel.connect()
                await ctx.reply(f"Connected to {channel.name}!")
            else: 
                vc = ctx.voice_client
            sound_file = sounds.get(sound.lower())
            if not sound_file:
                await ctx.reply(f"Sound '{sound}' not found.")
                await vc.disconnect()
                return
            vc.play(discord.FFmpegPCMAudio(f"{sound_directory}/{sound_file}"))
            while vc.is_playing():
                await sleep(2)
            await vc.disconnect()
        except Exception as e:
            await ctx.reply(f"Error connecting to voice channel: {e}")
    else:
        await ctx.reply("You must be in a voice channel to use this command.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send(f"Disconnected from voice channel")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def list(ctx):
    await ctx.send("Available sounds:\n" + "\n".join(f"- {sound}" for sound in sounds.keys()))

bot.run(token,log_handler=handler, log_level=logging.DEBUG)