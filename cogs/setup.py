import discord
from discord.ext import commands
from embed import em

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__name__ = "Setup Commands"
        self.__description__ = "These commands will let you setup and manage your servers settings for the captcha"
 

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        await ctx.send(embed=em("Ooops!", "Custom setup is comming soon!"))


def setup(bot):
    bot.add_cog(Setup(bot))