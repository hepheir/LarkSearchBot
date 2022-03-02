import logging

from discord import Intents
from discord import Game
from discord.ext.commands import Bot


COMMAND_PREFIX = "!"
HELP_COMMAND = "도움말"
TOKEN = "TOKEN"

intents = Intents.default()
bot = Bot(command_prefix=COMMAND_PREFIX,
          intents=intents)

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(activity=Game(name=f"{COMMAND_PREFIX}{HELP_COMMAND}"))

bot.run(TOKEN)
