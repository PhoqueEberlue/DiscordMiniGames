from discord.ext import commands
import discord
from .slapz import slapz
from .player import player
from asyncio import TimeoutError
from random import choice

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
        strPlayerList = ''
        async for user in reac.users():
            if user != self.bot.user:
                players.append(player(user))
                strPlayerList += f' {user.mention} |'
        game = slapz(players)
        while(not game.getEnd()):
            currentPlayer = game.nextPlayer()
            await ctx.send(f'{currentPlayer.getUser().mention}\'s turn')
            await ctx.send(f'Inventory: {currentPlayer.getInventory()}, HP: {currentPlayer.getHp()}')
            await ctx.send('Chose your action: move or pass')
            command = ""
            try:
                msg = await self.bot.wait_for('message', check=lambda message: message.author == currentPlayer.getUser() and ctx.channel == message.channel, timeout=10)
                command = msg.content
            except TimeoutError:
                command = choice(["m", "p"])
            if command in ["move", "m", "1"]:
                action = game.Move(currentPlayer)
                if action[0] == "fight":
                    game.fight(action[1])
                if action[0] == "loot":
                    await ctx.send(f'you looted {action[1]}')
                if action[0] == "full":
                    await ctx.send("your inventory is full")
            elif command in ["pass", "p", "2"]:
                pass
                
            

def setup(bot):
    bot.add_cog(Slapz(bot))
