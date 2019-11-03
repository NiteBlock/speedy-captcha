import json
from datetime import datetime as dt
import discord
with open("config.json", encoding="utf8") as f:
    config = json.loads(f.read())
    defaultEmbed = config["embed"]

def em(title, description, color=defaultEmbed["color"], footer=defaultEmbed["footer"], thumbnail=defaultEmbed["thumbnail"]):
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    if isinstance(color, discord.Colour):
        embed.colour = color
    else:
        embed.colour = discord.Colour(color)
    embed.timestamp = dt.utcnow()
    embed.set_footer(text=footer)
    embed.set_thumbnail(url=thumbnail)
    return embed