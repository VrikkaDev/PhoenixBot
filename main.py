# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import CommandUtils
import FileUtils
import MessageUtils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intent = discord.Intents.all()

bot = commands.Bot(command_prefix='/')

global textResponses
textResponses = FileUtils.json_to_dict("textresponses.json")

MessageUtils.Init(textResponses)

global commandResponses
commandResponses = FileUtils.json_to_dict("botcommands.json")

CommandUtils.Init(commandResponses, bot)


@bot.event
async def on_ready():
    print(f'{bot.user} is connected and running')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    a = MessageUtils.NeedToAnswer(message)

    if not a.willRespond:
        return

    await message.channel.send(a.respondText)


bot.run(TOKEN)