from discord.ext import commands

global cr, bot
cr = {}
bot = None


def Init(_commandResponses, _bot):
    global cr, bot
    cr = _commandResponses
    bot = _bot

    register_commands()


def register_commands():
    for key in cr.keys():
        value = cr[key]

        @bot.command(name=str(key), help=str(value["help"]))
        @commands.has_role(value["role_needed"])
        async def execute(ctx):
            print("a")
            response = value["response"]
            await ctx.send(response)

    @bot.command(name="mrtest")
    async def exec(ctx):
        await ctx.send("yeeaah")