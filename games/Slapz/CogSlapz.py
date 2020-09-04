from discord.ext import commands
from PIL import Image
import requests
import discord

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
        i = 0
        for user in players:
            response = requests.get(f"{user.avatar_url}")
            file = open(f"{i}.webp", "wb")
            file.write(response.content)
            file.close()
            im = Image.open(f"{i}.webp").convert("RGBA")
            new_im = im.resize((128,128))
            bg = Image.open("./games/Slapz/img/background.png")
            bg.paste(new_im, (181,181), new_im)
            ch = Image.open("./games/Slapz/img/character.png")
            bg.paste(ch, (0,0), ch)
            bg.save(f"{i}.png", "png")
            await ctx.send(file=discord.File(f'{i}.png'))
            i+=1
        '''
        end = False
        while(not end):
            pass
        '''

def setup(bot):
    bot.add_cog(Slapz(bot))