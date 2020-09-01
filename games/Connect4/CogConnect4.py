from discord.ext import commands

class Connect4(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def power4(self, ctx: commands.Context):
        await ctx.send("Party created, click on the reaction bellow to join!")
        partyMessage = ctx.channel.last_message
        await partyMessage.add_reaction("✅")

    @commands.command()
    async def playpower4(self, ctx: commands.Context):
        reac = None
        players = []
        async for message in ctx.channel.history(limit=100):
            if message.author == bot.user:
                reac = message.reactions[0]
                break
        try:
            players.append(reac.users()[1])
            players.append(reac.users()[2])
            await ctx.send(players)
        except:
            await ctx.send("frero y'a pas de joueurs qu'est-ce que tu fait là ?")
        await ctx.send(f'joueur 1 : {players[0].mention} joueur 2 : {players[1].mention}')
        end = False
        while(not end):
            pass

def setup(bot):
    bot.add_cog(BombParty(bot))   