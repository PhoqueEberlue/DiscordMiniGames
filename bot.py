import discord
import json
from discord.ext import commands
from token import token

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('bot is ready')

################### SETTINGS RELATED ###################
Languages = ["fr", "en"]

def getSettings(GuildId):
    file_name = './settings/' + str(GuildId) + '.json'
    try:
        with open(file_name, "r", encoding="utf-8") as read_file:
            settings = json.load(read_file)
    except:
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
        channel = f'discord-bomb-party-{i}'
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
            await ctx.guild.create_text_channel(f'discord-bomb-party-{i}')
            i += 1
        await ctx.send(f'{arg} channels have been created.')
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
                if f'discord-bomb-party-{i}' == channel.name:
                    await channel.delete()
                    i -= 1
                    break  
        await ctx.send(f'{arg} channels have been deleted.')
    else:
        await ctx.send('You can\'t delete more than 50 or less than 1 channels at once')
################### END OF CHANNELS RELATED ####################

################### ROLES RELATED ####################

################### END OF ROLES RELATED ####################

bot.run(token())