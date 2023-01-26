# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import CommandUtils
import ConfigUtils
import FileUtils
import MessageUtils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ConfigUtils.Init()

intent = discord.Intents.all()

bot = commands.Bot(
    command_prefix='/',
    intents=intent
)

tree = bot.tree

global textResponses
textResponses = FileUtils.json_to_dict("textresponses.json")

MessageUtils.Init(textResponses)

global commandResponses
commandResponses = FileUtils.json_to_dict("botcommands.json")

CommandUtils.Init(commandResponses, bot, tree)


@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=ConfigUtils.GetGuild()))

    activity = discord.Game(name="PhoenixSMP", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print(f'{bot.user} is connected and running')


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    a = MessageUtils.NeedToAnswer(message)

    if not a.willRespond:
        await bot.process_commands(message)
        return

    await bot.process_commands(message)
    await message.channel.send(a.respondText)


bot.run(TOKEN)
