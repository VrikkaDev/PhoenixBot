from discord.ext import commands
import discord
from typing import Union

import ConfigUtils

global cr, bot, tree
cr = {}
bot: Union[commands.Bot, None] = None
tree = None


def Init(_commandResponses, _bot, _tree):
    global cr, bot, tree
    cr = _commandResponses
    bot = _bot
    tree = _tree

    register_commands()


def _getChannels_(value) -> list:
    return list(value["allowed_channels"].keys())


def _hasRole_(value, roles: discord.Member) -> bool:

    r = False
    needed = str(value["role_needed"])

    i: discord.Role
    for i in roles:
        if str(i.id) == needed:
            r = True
            break

    return r


def register_commands():
    for key in cr.keys():
        value = cr[key]

        @tree.command(
            name=str(key),
            description=str(value["description"]),
            guild=discord.Object(id=ConfigUtils.GetGuild())
        )
        async def execute(ctx: discord.Interaction):

            val = cr[ctx.command.name]

            if not _hasRole_(val, ctx.user.roles):
                await ctx.response.send_message("You do not have the required role to execute this command.")
                return

            if not _getChannels_(val).__contains__(str(ctx.channel_id)):
                await ctx.response.send_message("This command is not available in this channel. Please try a different "
                                                "command or channel.")
                return

            response = val["response"]
            await ctx.response.send_message(response)
