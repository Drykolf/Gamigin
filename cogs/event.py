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
    
    ''' @commands.Cog.listener()
    async def on_member_join(self, member):
        async with self.bot.db_pool.acquire() as conn:
            result = await conn.fetchrow("SELECT serverid, join_role, join_message, leave_message, moderation_logs, welcome_logs FROM setupBot WHERE serverID = $1", member.guild.id)
            guild_config = dict(result) if result else None
            async with self.bot.db_pool.acquire() as connection:
            await connection.execute("DELETE FROM setup_bot WHERE server_id = $1", guild.id)
        print(guild_config)
        if guild_config:
            #...'
    '''
async def setup(bot):
    await bot.add_cog(EventHandlers(bot))