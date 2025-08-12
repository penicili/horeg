import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests

# load .evn
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "job" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} J word are prohibited in this channel")
    
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {ctx.author.mention}')

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

bot.run(token,log_handler=handler, log_level=logging.DEBUG)