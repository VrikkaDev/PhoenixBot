import os

global GUILD
GUILD = 0


def Init():
    global GUILD
    GUILD = os.getenv('DISCORD_GUILD')


def GetGuild() -> int:
    return GUILD
