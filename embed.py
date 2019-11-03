import json
from datetime import datetime as dt
import discord
with open("config.json") as f:
    config = json.loads(f.read())
    defaultEmbed = config["embed"]

def em(title, description, color=defaultEmbed["color"], footer=defaultEmbed["footer"], thumbnail=defaultEmbed["thumbnail"]):
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    if isinstance(color, discord.Color):
        embed.color = color
    else:
        embed.color = discord.Color(color)
    embed.timestamp = dt.utcnow()
    embed.set_footer(text=footer)
    embed.set_thumbnail(url=thumbnail)
    return embed