import os
from discord.ext import commands
from tokenConfig import getToken

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('bot is ready')
    
@bot.event
async def on_guild_join(self, guild):
    await guild.create_role(name="Discord Mini Games Admin")

@bot.command()
async def load(ctx: commands.Context, extension):
    if ctx.author.id == 205434999888019456:
        try:
            bot.load_extension(f'games.{extension}.Cog{extension}')
            await ctx.send(f'{extension} module has been loaded')
        except ModuleNotFoundError as error:
            await ctx.send(error)

@bot.command()
async def unload(ctx: commands.Context, extension):
    if ctx.author.id == 205434999888019456:
        try:
            bot.unload_extension(f'games.{extension}.Cog{extension}')
            await ctx.send(f'{extension} module has been unloaded')
        except commands.errors.ExtensionNotLoaded as error:
            await ctx.send(error)
            
@bot.command()
async def refresh(ctx: commands.Context, extension):
    if ctx.author.id == 205434999888019456:
        try:
            bot.unload_extension(f'games.{extension}.Cog{extension}')
            bot.load_extension(f'games.{extension}.Cog{extension}')
            await ctx.send(f'{extension} module has been refreshed')
            #await load(ctx, extension)
        except commands.errors.ExtensionNotLoaded as error:
            await ctx.send(error)

#Loads up every cogs in the ./games file
for rep in os.listdir('./games'):
    for file_name in os.listdir('./games/' + rep):
        if file_name.startswith('Cog') and file_name.endswith('.py'):
            bot.load_extension(f'games.{rep}.{file_name[:-3]}')

bot.run(getToken())