import time
import json
import random
from .PlayerList import PlayerList
from .Player import Player
from discord.ext import commands

class BombParty(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        ############### CONSTANT POULE ###############
        self._channelPrefix = 'bomb-party-'
        self._languages = ["fr", "en"]
        with open('Dictionnaries.json', "r", encoding="utf-8") as read_file:
            self._dictionnaries = json.load(read_file)
        ############ ENDOF CONSTANT POULE ############

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await guild.create_role(name="Bomb Party Admin")
        # await guild.invoke(createChannel) #FIX THIS PLS
        
    ################ SETTINGS RELATED ################
    @staticmethod
    def isAdmin(Member):
        """
        parameter: Member
        return: a boolean that indicates if the Member has the Admin role
        """
        for role in Member.roles:
            if role.name == "Bomb Party Admin":
                return True
        return False
    
    @staticmethod
    def getSettings(GuildId):
        """
        parameter: GuildId
        return: a dictionnary that represent the settings of a server (if none settings has been changed it will use the default file) e.g: ./settings/DefaultSettings.json
        """
        file_name = './settings/' + str(GuildId) + '.json'
        try:
            with open(file_name, "r", encoding="utf-8") as read_file:
                settings = json.load(read_file)
        except FileNotFoundError:
            with open('./settings/DefaultSettings.json', "r", encoding="utf-8") as read_file:
                settings = json.load(read_file)
        return settings

    @staticmethod
    def setSettings(GuildId, settings):
        """
        parameter: GuildId, settings (dictionnary)
        """
        file_name = './settings/' + str(GuildId) + '.json'
        with open(file_name, "w", encoding="utf-8") as write_file:
            json.dump(settings, write_file)

    @commands.command()
    async def showSettings(self, ctx: commands.Context):
        """
        parameter: self, ctx 
        send a message showing the guild's settings
        """
        if self.isAdmin(ctx.author):
            settings = self.getSettings(ctx.guild.id)
            await ctx.send(f'Language: {settings["Language"]}\nMinimum timing of the bomb: {settings["MinimumTiming"]} seconds')

    @commands.command()
    async def setLanguage(self, ctx: commands.Context, arg):
        """
        parameter: self, ctx, arg (an element of self._languages)
        change the language setting of the guild
        """
        if self.isAdmin(ctx.author):
            settings = self.getSettings(ctx.guild.id)
            if arg in self._languages:
                settings["Language"] = arg
                setSettings(ctx.guild.id, settings)
                await ctx.send(f'Language have been set to {arg}')
            else:
                await ctx.send("This language isn't accepted, or maybe you misstyped it...")

    @commands.command()
    async def setTiming(self, ctx: commands.Context, arg):
        """
        parameter: self, ctx, arg (an integer)
        change the minimum timing of the bomb setting of the guild
        """
        if self.isAdmin(ctx.author):
            settings = self.getSettings(ctx.guild.id)
            arg = int(arg)
            if arg <= 10 and arg >= 0:
                settings["MinimumTiming"] = arg
                setSettings(ctx.guild.id, settings)
                await ctx.send(f'Time have been set to {arg} seconds')
            else:
                await ctx.send("You can only chose a number between 0 and 10.")
    ############# ENDOF SETTINGS RELATED #############

    ################ CHANNELS RELATED ################
    def getMaxChannel(self, channels):
        """
        parameter: self, channels (a list of channel)
        return: the highest textChannel of bomb party
        """
        i = 0
        done = True
        while(done):
            channel = self._channelPrefix + str(i)
            if channel in channels:
                i += 1
            else:
                done = False
        return i

    @staticmethod
    def getChannelNamesList(guild):
        """
        parameter: guild
        return a list of channel name in a given guild
        """
        channels = []
        for channel in guild.text_channels:
            channels.append(channel.name)
        return channels

    @commands.command()
    async def createChannel(self, ctx: commands.Context, arg=1):
        """
        parameter: self, ctx, arg (an integer)
        creates {arg} bomb party channel
        """
        if self.isAdmin(ctx.author):
            arg = int(arg)
            if arg <= 50 and arg >=1:
                channels = getChannelNamesList(ctx.guild)
                i = getMaxChannel(channels)
                for _ in range(arg):
                    await ctx.guild.create_text_channel(self._channelPrefix + str(i))
                    i += 1
                await ctx.send(f'{arg} channel(s) have been created.')
            else:
                await ctx.send('You can\'t create more than 50 or less than 1 channels at once')

    @commands.command()
    async def deleteChannel(self, ctx: commands.Context, arg=1):
        """
        parameter: self, ctx, arg (an integer)
        deletes {arg} bomb party channel
        """
        if self.isAdmin(ctx.author):
            arg = int(arg)
            if arg <= 50 and arg >=1:
                channels = getChannelNamesList(ctx.guild)
                i = getMaxChannel(channels) - 1
                for _ in range(arg):
                    for channel in ctx.guild.text_channels:
                        if self._channelPrefix + str(i) == channel.name:
                            await channel.delete()
                            i -= 1
                            break  
                await ctx.send(f'{arg} channel(s) have been deleted.')
            else:
                await ctx.send('You can\'t delete more than 50 or less than 1 channels at once')
    ############# ENDOF CHANNELS RELATED #############

    ################ ROLES RELATED ################
    @commands.command()
    async def createRoles(self, ctx: commands.Context):
        """
        parameter: self, ctx
        creates roles that are needed for the bot to work
        """
        if self.isAdmin(ctx.author):
            await ctx.guild.create_role(name="Bomb Party Admin")
    ############# ENDOF ROLES RELATED #############

    ################ PARTY RELATED ################
    @commands.command()
    async def party(self, ctx: commands.Context):
        """
        parameter: ctx, the context where the command is called
        This command check if the TextChannel where it is called starts with the _channelPrefix then create a party message if it is true
        """
        if ctx.channel.name[:-1] != self._channelPrefix:
            await ctx.send("You can't call this command outside a bomb-party channel!")
        else:
            await ctx.send("Party created, click on the reaction bellow to join!")
            partyMessage = ctx.channel.last_message
            await partyMessage.add_reaction("✅")

    @commands.command()
    async def play(self, ctx: commands.Context):
        """
        parameter: self, ctx
        Bomb party game itself, this function is absolutely massive and could be simplified for sure
        """
        channel = ctx.channel
        settings = self.getSettings(ctx.guild.id)
        lang = settings["Language"]
        minTiming = settings["MinimumTiming"]
        baseTiming = 15
        timeLeft = baseTiming
        reac = None
        players = PlayerList()
        strPlayerList = 'Players:'
        unavailableWords = set()
        partyFindBool = False
        async for message in ctx.channel.history(limit=200):
            if message.author == self.bot.user and message.content == "Party created, click on the reaction bellow to join!":
                reac = message.reactions[0]
                partyFindBool = True
                break
        if partyFindBool:
            async for user in reac.users():
                if user != self.bot.user:
                    players.appendPlayer(Player(user))
                    strPlayerList += f' {user.mention} |'
            if len(players) > 1:
                await ctx.send(strPlayerList)
                end = False
                while(not end):
                    CurrentPlayer = players.currentPlayer()
                    start = time.time()
                    letters = random.choice(self._dictionnaries[lang]["letters"])
                    await ctx.send(f'{CurrentPlayer.user().mention}, type a word that contains: **{letters}**')
                    if timeLeft < minTiming:
                        timeLeft = minTiming
                    explode = True
                    while(timeLeft - (time.time() - start) > 0):
                        time.sleep(0.1)
                        async for message in channel.history(limit=1):
                            lastMsg = message
                        lastMsgContent = lastMsg.content.lower()
                        if lastMsg.author == CurrentPlayer.user() and letters in lastMsgContent and lastMsgContent in self._dictionnaries[lang]["words"] and lastMsgContent not in unavailableWords:
                            unavailableWords.add(lastMsgContent)
                            explode = False
                            break
                    timeLeft = timeLeft - (time.time() - start)
                    if explode:
                        timeLeft = baseTiming
                        CurrentPlayer.decreaseLife()
                        if CurrentPlayer.life() <= 0:
                            players.removePlayer(CurrentPlayer)
                            await ctx.send(f'💥BOOM💥, player {CurrentPlayer.user().mention} haven\'t aswered as quickly enough!')
                        else:
                            await ctx.send(f'💥BOOM💥, player {CurrentPlayer.user().mention} has only {CurrentPlayer.life()} life remaining...')
                    players.increaseIndex()
                    if players.isEnd():
                        end = True
                await ctx.send(f'{players.getWinner().user().mention} has won! 🏆')
            else:
                await ctx.send(f'This party has been canceled as not enough players joined...')
        else:
            await ctx.send(f'No party have been created.')
    ############# ENDOF PARTY RELATED #############

def setup(bot):
    bot.add_cog(BombParty(bot))