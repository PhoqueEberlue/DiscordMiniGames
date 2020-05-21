import os
from discord.ext import commands
from tokenConfig import getToken

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('bot is ready')

@bot.command()
async def load(ctx: commands.Context, extension):
    if ctx.author.id == 205434999888019456:
        try:
            bot.load_extension(f'games.{extension}.Cog{extension}')
            await ctx.send(f'Le module {extension} à été load')
        except ModuleNotFoundError as error:
            await ctx.send(error)

@bot.command()
async def unload(ctx: commands.Context, extension):
    if ctx.author.id == 205434999888019456:
        try:
            bot.unload_extension(f'games.{extension}.Cog{extension}')
            await ctx.send(f'Le module {extension} à été unload')
        except commands.errors.ExtensionNotLoaded as error:
            await ctx.send(error)
            
@bot.command()
async def refresh(ctx: commands.Context, extension):
    if ctx.author.id == 205434999888019456:
        try:
            bot.unload_extension(f'games.{extension}.Cog{extension}')
            await load(ctx, extension)
        except commands.errors.ExtensionNotLoaded as error:
            await ctx.send(error)

#Loads up every cogs in the ./games file
for rep in os.listdir('./games'):
    for file_name in os.listdir('./games/' + rep):
        if file_name.startswith('Cog') and file_name.endswith('.py'):
            bot.load_extension(f'games.{rep}.{file_name[:-3]}') #Deletes the ".py" at the end of the filename

bot.run(getToken())