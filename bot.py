import discord  # unused cause lig 5
import json
import time     # unused
from random import randint
from discord.ext import commands
from tokenConfig import getToken

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('bot is ready')


@bot.event
async def on_guild_join(guild):
    await guild.create_role(name="Bomb Party Admin")
    await guild.create_role(name="BP Current Player")
    await guild.invoke(create_channel)


################ CONSTANT POULE ####################


ChannelPrefix = 'bomb-party-'
Languages = ["fr", "en"]


################ END OF CONSTANT POULE ####################


################### SETUP RELATED ###################


# @bot.command()
# async def quickSetup(ctx: commands.Context):
#     await ctx.invoke(createChannel)


################### SETUP RELATED ###################


################### SETTINGS RELATED ###################


def get_settings(GuildId):
    file_name = './settings/' + str(GuildId) + '.json'
    try:
        with open(file_name, "r", encoding="utf-8") as read_file:
            settings = json.load(read_file)
    except FileNotFoundError:
        with open('./settings/DefaultSettings.json', "r", encoding="utf-8") as read_file:
            settings = json.load(read_file)
    return settings


def set_settings(GuildId, settings):
    file_name = './settings/' + str(GuildId) + '.json'
    with open(file_name, "w", encoding="utf-8") as write_file:
        json.dump(settings, write_file)


@bot.command()
async def show_settings(ctx: commands.Context):
    settings = get_settings(ctx.guild.id)
    await ctx.send(f'Language: {settings["Language"]}\nMinimum timing of the bomb: {settings["MinimumTiming"]} seconds')


@bot.command()
async def set_language(ctx: commands.Context, arg):
    settings = get_settings(ctx.guild.id)
    if arg in Languages:
        settings["Language"] = arg
        set_settings(ctx.guild.id, settings)
        await ctx.send(f'Language have been set to {arg}')
    else:
        await ctx.send("This language isn't accepted, or maybe you misstyped it...")


@bot.command()
async def set_timing(ctx: commands.Context, arg):
    settings = get_settings(ctx.guild.id)
    arg = int(arg)
    if 10 >= arg >= 0:
        settings["MinimumTiming"] = arg
        set_settings(ctx.guild.id, settings)
        await ctx.send(f'Time have been set to {arg} seconds')
    else:
        await ctx.send("You can only chose a number between 0 and 10.")


############### END OF SETTINGS RELATED #################


################### CHANNELS RELATED ####################


def get_max_channel(channels):
    i = 0
    done = True
    while done:
        channel = ChannelPrefix + str(i)
        if channel in channels:
            i += 1
        else:
            done = False
    return i


def get_channel_names_list(guild):
    channels = []
    for channel in guild.text_channels:
        channels.append(channel.name)
    return channels


@bot.command()
async def create_channel(ctx: commands.Context, arg=1):
    arg = int(arg)
    if 50 >= arg >= 1:
        channels = get_channel_names_list(ctx.guild)
        i = get_max_channel(channels)
        for _ in range(arg):
            await ctx.guild.create_text_channel(ChannelPrefix + str(i))
            i += 1
        await ctx.send(f'{arg} channel(s) have been created.')
    else:
        await ctx.send('You can\'t create more than 50 or less than 1 channels at once')


@bot.command()
async def delete_channel(ctx: commands.Context, arg=1):
    arg = int(arg)
    if 50 >= arg >= 1:
        channels = get_channel_names_list(ctx.guild)
        i = get_max_channel(channels) - 1
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

# TODO finir l'attribution des rôles
@bot.command()
async def create_roles(ctx: commands.Context):
    await ctx.guild.create_role(name="Bomb Party Admin")
    await ctx.guild.create_role(name="BP Current Player")


################### END OF ROLES RELATED ####################

################### PARTY RELATED ####################
@bot.command()
async def party(ctx: commands.Context):
    """
    :param ctx: Le contexte
    :return: void
    Fonctione exécuté lors de la commande $party
    Elle vérifie si la commande est exec dans un channel bomb-party
    Si oui, envoie un message et ajoute un réaction
    """
    if ctx.channel.name[:-1] != ChannelPrefix:
        await ctx.send("You can't call this command outside a bomb-party channel!")
    else:
        await ctx.send("Party created, click on the reaction bellow to join!")
        partyMessage = ctx.channel.last_message
        await partyMessage.add_reaction('✅')


@bot.command()
async def play(ctx: commands.Context):
    counter = 0
    reac = None
    players = []

    async for message in ctx.channel.history(limit=100):  # recherche le message du bot avec la réaction ✅
        if message.author == bot.user:
            reac = message.reactions[0]
            break
    else:
        await ctx.send("Impossible de retrouver le dernier message du bot...")

    async for user in reac.users():  # ajoute les personnes qui ont réagi au msg dans [players]
        if user != bot.user:
            players.append(user)

    for player in players:  # attribution des rôles au personnes
        player.add_roles()  # TODO

    end = False
    Index = randint(0, len(players) - 1)
    CurrentPlayer = players[Index]
    while not end:
        CurrentPlayer.add_role()
    # while():


################## END OF PARTY RELATED ####################

# discord.on_reaction_add(reaction, user)
bot.run(getToken())
