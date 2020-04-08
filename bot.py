import discord
import json
import time
from discord.ext import commands
from tokenConfig import getToken
import random
from random import randint

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('bot is ready')

@bot.event
async def on_guild_join(guild):
    await guild.create_role(name="Bomb Party Admin")
    await guild.create_role(name="BP Current Player")
    await guild.invoke(createChannel)


################ CONSTANT POULE ####################
ChannelPrefix = 'bomb-party-'
Languages = ["fr", "en"]
with open('Dictionnaries.json', "r", encoding="utf-8") as read_file:
    Dictionnaries = json.load(read_file)
print(Dictionnaries['fr']['letters'])
################ END OF CONSTANT POULE ####################

################### SETUP RELATED ###################
# @bot.command()
# async def quickSetup(ctx: commands.Context):
#     await ctx.invoke(createChannel)
################### SETUP RELATED ###################

################### SETTINGS RELATED ###################
def getSettings(GuildId):
    file_name = './settings/' + str(GuildId) + '.json'
    try:
        with open(file_name, "r", encoding="utf-8") as read_file:
            settings = json.load(read_file)
    except FileNotFoundError:
        with open('./settings/DefaultSettings.json', "r", encoding="utf-8") as read_file:
            settings = json.load(read_file)
    return settings

def setSettings(GuildId, settings):
    file_name = './settings/' + str(GuildId) + '.json'
    with open(file_name, "w", encoding="utf-8") as write_file:
        json.dump(settings, write_file)

@bot.command()
async def showSettings(ctx: commands.Context):
    settings = getSettings(ctx.guild.id)
    await ctx.send(f'Language: {settings["Language"]}\nMinimum timing of the bomb: {settings["MinimumTiming"]} seconds')

@bot.command()
async def setLanguage(ctx: commands.Context, arg):
    settings = getSettings(ctx.guild.id)
    if arg in Languages:
        settings["Language"] = arg
        setSettings(ctx.guild.id, settings)
        await ctx.send(f'Language have been set to {arg}')
    else:
        await ctx.send("This language isn't accepted, or maybe you misstyped it...")

@bot.command()
async def setTiming(ctx: commands.Context, arg):
    settings = getSettings(ctx.guild.id)
    arg = int(arg)
    if arg <= 10 and arg >= 0:
        settings["MinimumTiming"] = arg
        setSettings(ctx.guild.id, settings)
        await ctx.send(f'Time have been set to {arg} seconds')
    else:
        await ctx.send("You can only chose a number between 0 and 10.")
############## END OF SETTINGS RELATED ################

################### CHANNELS RELATED ####################
def getMaxChannel(channels):
    i = 0
    done = True
    while(done):
        channel = ChannelPrefix + str(i)
        if channel in channels:
            i += 1
        else:
            done = False
    return i

def getChannelNamesList(guild):
    channels = []
    for channel in guild.text_channels:
        channels.append(channel.name)
    return channels

@bot.command()
async def createChannel(ctx: commands.Context, arg=1):
    arg = int(arg)
    if arg <= 50 and arg >=1:
        channels = getChannelNamesList(ctx.guild)
        i = getMaxChannel(channels)
        for _ in range(arg):
            await ctx.guild.create_text_channel(ChannelPrefix + str(i))
            i += 1
        await ctx.send(f'{arg} channel(s) have been created.')
    else:
        await ctx.send('You can\'t create more than 50 or less than 1 channels at once')

@bot.command()
async def deleteChannel(ctx: commands.Context, arg=1):
    arg = int(arg)
    if arg <= 50 and arg >=1:
        channels = getChannelNamesList(ctx.guild)
        i = getMaxChannel(channels) - 1
        for _ in range(arg):
            for channel in ctx.guild.text_channels:
                if ChannelPrefix + str(i) == channel.name:
                    await channel.delete()
                    i -= 1
                    break  
        await ctx.send(f'{arg} channel(s) have been deleted.')
    else:
        await ctx.send('You can\'t delete more than 50 or less than 1 channels at once')
################### END OF CHANNELS RELATED ####################

################### ROLES RELATED ####################
@bot.command()
async def createRoles(ctx: commands.Context):
    await ctx.guild.create_role(name="Bomb Party Admin")
    await ctx.guild.create_role(name="BP Current Player")
################### END OF ROLES RELATED ####################

################### PARTY RELATED ####################
@bot.command()
async def party(ctx: commands.Context):
    if ctx.channel.name[:-1] != ChannelPrefix:
        await ctx.send("You can't call this command outside a bomb-party channel!")
    else:
        await ctx.send("Party created, click on the reaction bellow to join!")
        partyMessage = ctx.channel.last_message
        await partyMessage.add_reaction("✅")

@bot.command()
async def play(ctx: commands.Context):
    winner = None
    channel = ctx.channel
    settings = getSettings(ctx.guild.id)
    lang = settings["Language"]
    minTiming = settings["MinimumTiming"]
    timeLeft = 15
    reac = None
    players = []
    unavailableWords = {}
    async for message in ctx.channel.history(limit=100):
        if message.author == bot.user:
            reac = message.reactions[0]
            break
    async for user in reac.users():
        if user != bot.user:
            players.append(user)
    # for player in players:
    #     player.add_roles()
    end = False
    Index = randint(0, len(players)-1)
    while(not end):
        survive = False
        CurrentPlayer = players[Index]
        #CurrentPlayer.add_role()
        start = time.time()
        letters = random.choice(Dictionnaries[lang]["letters"])
        await ctx.send(f'@{CurrentPlayer.name},type a word that contains: {letters}')
        if timeLeft < minTiming:
            timeLeft = minTiming
        while(timeLeft - (time.time() - start) > 0):
            lastMsg = channel.last_message
            lastMsgContent = lastMsg.content.lower()
            if lastMsg.author == CurrentPlayer and letters in lastMsgContent and lastMsgContent in Dictionnaries[lang]["words"] and lastMsgContent not in unavailableWords:
                unavailableWords.add(lastMsgContent) 
                survive = True
                break
        timeLeft = timeLeft - (time.time() - start)
        if not survive:
            players.remove(CurrentPlayer)
            await ctx.send(f'💥BOOM💥, player @{CurrentPlayer.name} haven\'t aswered as quickly enough!')
        if Index == len(players)-1:
            Index = 0
        else:
            Index += 1
        if len(players) == 1:
            end = True
            winner = CurrentPlayer 
    await ctx.send(f'@{winner.name} has won! 🏆')

################## END OF PARTY RELATED ####################

#discord.on_reaction_add(reaction, user)
bot.run(getToken())