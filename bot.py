import discord
from discord.ext import commands
from embed import em
import json
from glob import glob


class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"`{self.clean_prefix}{command.qualified_name} {command.signature}`\n"

    async def send_command_help(self, command):
        embed = em(command.name, command.description)
        if len(command.aliases) > 0:
            embed.add_field(name="Aliases", value=', '.join(command.aliases))
        embed.add_field(
            name="Usage", value=self.get_command_signature(command))
        await self.context.send(embed=embed)

    def get_embeds(self, mapping):
        new = []
        for cog, commands in mapping.items():
            if cog:
                if not hasattr(cog, "__name__"):
                    continue
                embed = em(cog.__name__, cog.__description)
                signitures = "\n".join(
                    [self.get_command_signature(c) for c in commands])
                if signitures:
                    embed.add_field(name="Command Usage", value=signitures)
                new.append(embed)
            else:
                embed = em("Speedy Captcha",
                           self.context.bot.config["description"])
                signitures = "\n".join(
                    [self.get_command_signature(c) for c in commands])
                if signitures:
                    embed.add_field(name="Command Usage", value=signitures)
                new.append(embed)
        return list(reversed(new))

    def get_category_message(self, mapping, page=0):
        embeds = self.get_embeds(mapping)
        total = len(embeds)
        embed = embeds[page]
        embed.set_footer(text=f"Page {page +1} of {total}")
        return embed

    async def send_bot_help(self, mapping):
        await self.context.message.delete()
        config = self.context.bot.config
        page = 0
        embed = self.get_category_message(mapping)
        reactions = [config['emojis']["info"], config['emojis']["forwards"], config['emojis']
                     ["quit"], config['emojis']["backwards"], config['emojis']["numberChoice"]]
        msg = await self.context.send(embed=embed)

        while True:
            try:
                for r in reactions:
                    await msg.add_reaction(r)

                def check(r, u):
                    return str(r.emoji) in reactions and u.id == self.context.author.id and r.message.id == msg.id
                r, u = await self.context.bot.wait_for("reaction_add", check=check)
                await msg.clear_reactions()
                if str(r.emoji) == config['emojis']["quit"]:
                    break
                if str(r.emoji) == config['emojis']["info"]:
                    prev = msg.embeds[0]
                    await msg.edit(embed=em(self.context.bot, f"To move pages use the {config['emojis']['forwards']} and {config['emojis']['backwards']}\nTo quit using the {config['emojis']['quit']} emoji\nTo go to a certain page use the {config['emojis']['numberChoice']} emoji!", "How to use the help menu!", footer="This message will be reset in 5 seconds..."))
                    await asyncio.sleep(5)
                    await msg.edit(embed=prev)
                if str(r.emoji) == config['emojis']["forwards"]:
                    if page == len(self.get_embeds(mapping)) - 1:
                        continue
                    page += 1
                    await msg.edit(embed=self.get_category_message(mapping, page))
                if str(r.emoji) == config['emojis']["backwards"]:
                    if page == 0:
                        continue
                    page -= 1
                    await msg.edit(embed=self.get_category_message(mapping, page))
                if str(r.emoji) == config['emojis']["numberChoice"]:
                    prev = msg.embeds[0]
                    await msg.edit(embed=em(self.context.bot, "Enter your number!", "Choose a page!", footer="This message will be reset in 10 seconds..."))

                    def check(message):
                        return message.author.id == self.context.author.id and message.channel == self.context.channel
                    try:
                        m = await self.context.bot.wait_for("message", check=check, timeout=10.1)
                    except asyncio.TimeoutError:
                        await msg.edit(embed=prev)
                        continue
                    try:
                        p = int(m.content)
                    except:
                        await msg.edit(embed=prev)
                        continue
                    if p > 0 and p <= len(self.get_embeds(mapping)):
                        page = p - 1
                        await m.delete()
                        await msg.edit(embed=self.get_category_message(mapping, page))
                    else:
                        await msg.edit(embed=prev)
            except Exception as e:
                print(e)
        await msg.delete()


class Bot(commands.Bot):
    def __init__(self, **kw):
        with open("config.json") as f:
            self.config = json.loads(f.read())
        kw["help_command"] = Help()
        super().__init__(self.config["prefix"], **kw)


"""
Running the Bot
"""

bot = Bot()


for file in glob("cogs/*.py"):
    file = file.replace(".py", "")
    file = file.replace("\\", ".")
    file = file.replace("/", ".")
    bot.load_extension(file)
bot.run(bot.config["token"])
