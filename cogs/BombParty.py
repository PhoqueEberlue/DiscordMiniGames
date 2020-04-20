import time
import json
import random
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
        await guild.create_role(name="BP Current Player")
        # await guild.invoke(createChannel) #FIX THIS PLS
        
    ################ SETTINGS RELATED ################
    @staticmethod
    def getSettings(GuildId):
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
        file_name = './settings/' + str(GuildId) + '.json'
        with open(file_name, "w", encoding="utf-8") as write_file:
            json.dump(settings, write_file)

    @commands.command()
    async def showSettings(self, ctx: commands.Context):
        settings = self.getSettings(ctx.guild.id)
        await ctx.send(f'Language: {settings["Language"]}\nMinimum timing of the bomb: {settings["MinimumTiming"]} seconds')

    @commands.command()
    async def setLanguage(self, ctx: commands.Context, arg):
        settings = self.getSettings(ctx.guild.id)
        if arg in self._languages:
            settings["Language"] = arg
            setSettings(ctx.guild.id, settings)
            await ctx.send(f'Language have been set to {arg}')
        else:
            await ctx.send("This language isn't accepted, or maybe you misstyped it...")

    @commands.command()
    async def setTiming(self, ctx: commands.Context, arg):
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
        channels = []
        for channel in guild.text_channels:
            channels.append(channel.name)
        return channels

    @commands.command()
    async def createChannel(self, ctx: commands.Context, arg=1):
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
        await ctx.guild.create_role(name="Bomb Party Admin")
        await ctx.guild.create_role(name="BP Current Player")
    ############# ENDOF ROLES RELATED #############

    ################ PARTY RELATED ################
    @commands.command()
    async def party(self, ctx: commands.Context):
        """
        param: ctx, the context where the command is called
        return: void
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
        winner = None
        channel = ctx.channel
        settings = self.getSettings(ctx.guild.id)
        lang = settings["Language"]
        minTiming = settings["MinimumTiming"]
        baseTiming = 15
        timeLeft = baseTiming
        reac = None
        players = [] #e.g: [{"User": userInstance1, "Life": 2}, {"User": userInstance2, "Life": 2}, {"User": userInstance1, "Life": 1}]
        strPlayerList = 'Players:'
        unavailableWords = set()
        async for message in ctx.channel.history(limit=100):
            if message.author == self.bot.user and message.content == "Party created, click on the reaction bellow to join!":
                reac = message.reactions[0]
                break
        async for user in reac.users():
            if user != self.bot.user:
                players.append({"User": user, "Life": 2})
                strPlayerList += f' {user.mention} |'
        await ctx.send(strPlayerList)
        # for player in players:
        #     player.add_roles()
        end = False
        Index = random.randint(0, len(players)-1)
        if len(players) <= 1:
                end = True
        while(not end):
            CurrentPlayer = players[Index]
            #CurrentPlayer.add_role()
            start = time.time()
            letters = random.choice(self._dictionnaries[lang]["letters"])
            await ctx.send(f'{CurrentPlayer["User"].mention}, type a word that contains: **{letters}**')
            if timeLeft < minTiming:
                timeLeft = minTiming
            explode = True
            while(timeLeft - (time.time() - start) > 0):
                async for message in channel.history(limit=1):
                    lastMsg = message
                lastMsgContent = lastMsg.content.lower()
                if lastMsg.author == CurrentPlayer["User"] and letters in lastMsgContent and lastMsgContent in self._dictionnaries[lang]["words"] and lastMsgContent not in unavailableWords:
                    unavailableWords.add(lastMsgContent)
                    explode = False
                    break
            timeLeft = timeLeft - (time.time() - start)
            if explode:
                timeLeft = baseTiming
                CurrentPlayer["Life"] -= 1
                if CurrentPlayer["Life"] <= 0:
                    players.remove(CurrentPlayer)
                    await ctx.send(f'💥BOOM💥, player {CurrentPlayer["User"].mention} haven\'t aswered as quickly enough!')
                    if Index >= len(players) - 1:
                        Index = 0
                else:
                    await ctx.send(f'💥BOOM💥, player {CurrentPlayer["User"].mention} has only {CurrentPlayer["Life"]} life remaining...')
                    if Index >= len(players) - 1:
                        Index = 0
                    else:
                        Index += 1
            else:
                if Index >= len(players) - 1:
                    Index = 0
                else:
                    Index += 1
            if len(players) == 1:
                end = True
        if len(players) == 0:
            await ctx.send(f'This party has been canceled as not enough players joined...')
        else:
            await ctx.send(f'{players[0]["User"].mention} has won! 🏆')
    ############# ENDOF PARTY RELATED #############

def setup(bot):
    bot.add_cog(BombParty(bot))