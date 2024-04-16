from discord.ext import commands
from discord import Embed, Member

class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('RPG cog is ready!')
    
    @commands.command()
    async def test(self, ctx):
        '''This is a test command'''
        if ctx.guild in self.allowedGuilds:
            await ctx.send(f'test')
        else:
            pass

async def setup(bot):
    await bot.add_cog(RPG(bot))