import os
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

#Loads up every cogs in the ./games file
for rep in os.listdir('./games'):
    for file_name in os.listdir('./games/' + rep):
        if file_name.startswith('Cog') and file_name.endswith('.py'):
            bot.load_extension('games.' + rep + f'.{file_name[:-3]}') #Deletes the ".py" at the end of the filename

bot.run(getToken())