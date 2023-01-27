from discord.ext import commands
import discord
from typing import Union

from discord.ext.commands._types import Check

import ConfigUtils
import MessageUtils

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


def _get_channels_(value) -> dict:
    return value["allowed_channels"]


def _create_channel_mention_(ids: list) -> str:
    r = ""
    for _id in ids:
        r += ("<#" + _id + ">" + " ,")
    r = r[:-1]
    return r


def _get_roles_(value) -> dict:
    return value["role_needed"]


def _has_role_(value, roles: discord.Member) -> bool:
    r = False
    needed = _get_roles_(value).keys()

    for x in needed:
        i: discord.Role
        for i in roles:
            if str(i.id) == str(x):
                r = True
                break
        if r:
            break

    return r


def register_commands():
    for key in cr.keys():
        value = cr[key]

        @tree.command(
            name=str(key),
            description=str(value["description"]),
            guild=discord.Object(id=ConfigUtils.GetGuild()),
        )
        async def execute(ctx: discord.Interaction):

            val = cr[ctx.command.name]

            if not _has_role_(val, ctx.user.roles):
                await ctx.response.send_message("You do not have the required role to execute this command.")
                return

            channels: dict = _get_channels_(val)

            channeltexts: list = _create_channel_mention_(channels.keys())

            if not channels.keys().__contains__(str(ctx.channel_id)):
                await ctx.response.send_message("This command is not available in this channel."
                                                " Please use this command in " + str(channeltexts))
                return

            response = val["response"]

            if MessageUtils.Lowercase(response["embedded"]) == "false":
                await ctx.response.send_message(response["text"])
                return
            embed = discord.Embed(title=response["text"], url=response["link"],
                                  description=response["embedded_description"],
                                  color=discord.Color.from_str(response["color"]))
            await ctx.response.send_message(embed=embed)
