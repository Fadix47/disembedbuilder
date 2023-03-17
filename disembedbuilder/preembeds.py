from discord import Embed, Colour

def error_embed(content) -> Embed:
    embed = Embed(description=content, colour=Colour.red())
    embed.set_author(name="ERROR", icon_url="https://media.discordapp.net/attachments/1022216775707938926/1086244881825005568/16790513415095641.png")
    return embed

def success_embed(content) -> Embed:
    embed = Embed(description=content, colour=Colour.green())
    embed.set_author(name="SUCCESS", icon_url="https://media.discordapp.net/attachments/1022216775707938926/1086244882064097310/16790513415095641.png")
    return embed

def info_embed(content) -> Embed:
    embed = Embed(description=content, colour=int("2B2D31", 16))
    return embed
