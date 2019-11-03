import discord
from discord.ext import commands
from embed import em
from captcha import gen_captcha

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__name__ = "Verify Commands"
        self.__description__ = "These commands will let you veirfy your account to get the member role!"
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        hardness = 3
        string, path, color = gen_captcha(hardness)
        color = discord.Colour.from_rgb(*color)
        try:
            embed = em("Verify your account", "Please reply with the code you see in the image below", color=color, footer=f"You have {0-hardness+6} mins to respond")
            embed.set_image(url="attachment://captcha.png")
            await member.send(embed=embed, file=discord.File(path, "captcha.png"))
        except:
            return
        def check(message):
            if not message.content == string and message.author.id == member.id :
                self.bot.loop.create_task(self.tell_member_they_failed(member))
                return False
            return message.author.id == member.id 
        message = await self.bot.wait_for("message", check=check)
        await member.send(embed=em("Compleated", "The captcha has been compleated and you have recived the role!"))
        role = discord.utils.get(member.guild.roles, name="Member")
        if role:
            await member.add_roles(role)
    async def tell_member_they_failed(self, member):
        await member.send(embed=em("Oops!", "You failed the captcha, please try again"))

def setup(bot):
    bot.add_cog(Verify(bot))