from discord.ext import commands
import discord
from .slapz import slapz

class Slapz(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._createMsg = "Click on the reaction to join the Slapz game!"

    @commands.command()
    async def slapz(self, ctx: commands.Context):
        await ctx.send(self._createMsg)
        partyMessage = ctx.channel.last_message
        await partyMessage.add_reaction("✅")

    @commands.command()
    async def playslapz(self, ctx: commands.Context):
        reac = None
        players = []
        async for message in ctx.channel.history(limit=100):
            if message.author == self.bot.user and message.content == self._createMsg:
                reac = message.reactions[0]
                break
        async for user in reac.users():
            if user != self.bot.user:
                players.append(user)
                #await ctx.send(user.avatar_url)
                #players.appendPlayer(Player(user))
                #strPlayerList += f' {user.mention} |'
                
        #msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        game = slapz(players)
        '''
        end = False
        while(not end):
            pass
        '''

def setup(bot):
    bot.add_cog(Slapz(bot))