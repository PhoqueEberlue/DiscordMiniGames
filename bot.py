import os
import json
import time
import random
from discord.ext import commands
from tokenConfig import getToken

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('bot is ready')

# @bot.command()
# async def load(ctx: commands.Context, extension):
#     bot.load_extension(f'cogs.{extension}')

# @bot.command()
# async def unload(ctx: commands.Context, extension):
#     bot.unload_extension(f'cogs.{extension}')


#Loads up every cogs in the ./cogs file
for file_name in os.listdir('./cogs'):
    if file_name.endswith('.py'):
        bot.load_extension(f'cogs.{file_name[:-3]}')

bot.run(getToken())