import discord
from discord.ext import commands

class EventHandlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        #...
        print(f'Logged in as {self.bot.user}')
        await self.bot.change_presence(activity=discord.Game("Probando..."))
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        pass
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        pass
    
async def setup(bot):
    await bot.add_cog(EventHandlers(bot))