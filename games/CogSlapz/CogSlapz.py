from discord.ext import commands

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
            if message.author == bot.user and message.content == self._createMsg:
                reac = message.reactions[0]
                break
        async for user in reac.users():
            if user != self.bot.user:
                pass
                #players.appendPlayer(Player(user))
                #strPlayerList += f' {user.mention} |'
        end = False
        while(not end):
            pass

def setup(bot):
    bot.add_cog(Slapz(bot))