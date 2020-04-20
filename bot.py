import json
import time
import os
from discord.ext import commands
from tokenConfig import getToken
import random

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('bot is ready')

@bot.event
async def on_guild_join(guild):
    await guild.create_role(name="Bomb Party Admin")
    await guild.create_role(name="BP Current Player")
    # await guild.invoke(createChannel) #FIX THIS PLS

@bot.command()
async def load(ctx: commands.Context, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx: commands.Context, extension):
    bot.unload_extension(f'cogs.{extension}')

for file_name in os.listdir('./cogs'):
    if file_name.endswith('.py'):
        bot.load_extension(f'cogs.{file_name[:-3]}')

###################################################################### POWER 4 ######################################################################
# @bot.command()
# async def power4(ctx: commands.Context):
#     await ctx.send("Party created, click on the reaction bellow to join!")
#     partyMessage = ctx.channel.last_message
#     await partyMessage.add_reaction("✅")

# @bot.command()
# async def playPower4(ctx: commands.Context):
#     reac = None
#     players = []
#     async for message in ctx.channel.history(limit=100):
#         if message.author == bot.user:
#             reac = message.reactions[0]
#             break
#     try:
#         players.append(reac.users()[1])
#         players.append(reac.users()[2])
#         await ctx.send(players)
#     except:
#         await ctx.send("frero y'a pas de joueurs qu'est-ce que tu fait là ?")
#     await ctx.send(f'joueur 1 : {players[0].mention} joueur 2 : {players[1].mention}')
#     end = False
#     while(not end):
#         pass
################################################################### ENDOF POWER 4 ###################################################################

bot.run(getToken())