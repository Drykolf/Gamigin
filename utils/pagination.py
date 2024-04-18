import traceback
from typing import Any, Dict, Optional
from discord import Embed, HTTPException, Interaction, ui, ButtonStyle, Colour, utils, Message
from discord.ext import menus, commands

class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, items):
        embed = Embed(title='EMBED')
        for reg in items:
            embed.add_field(name=reg[0],value=reg[1], inline=False)
        # you can format the embed however you'd like
        return embed

class CapacitiesPageSource(menus.ListPageSource):
    async def format_page(self, menu, items):
        embed = Embed(title='Dino Capacities and Roll Checks', description='''
                      These are the extra abilities and roll checks Dinos can have in the story event. 
                      This is just an extensive list of all known capacities and roll checks dinos can have for reference. 
                      No Dino will have access to most of these. All roll checks cost Special Ability Points (SAP) to use them, and capacities may require them.''')
        for reg in items:
            embed.add_field(name=reg[0],value=reg[1], inline=False)
        # you can format the embed however you'd like
        return embed
    
class PlayersPageSource(menus.ListPageSource):
    async def format_page(self, menu, items):
        embed = Embed(title='Event participants', description='Brave players of the rpg event')
        for reg in items:
            info:str = f'Chosen dino **{reg[1]}**, and its great name **{reg[2]}**'
            embed.add_field(name=reg[0],value=info, inline=False)
        # you can format the embed however you'd like
        return embed