import asyncio
import os
from typing import List
from discord.ext import commands
import asyncpg
from discord import Intents
import utils.settings as settings
from utils.bot import Gamigin

'''async def get_server_prefix(client, message):
    async with self.bot.db_pool.acquire() as conn:
    result = await conn.fetchrow("SELECT serverid, join_role, join_message, leave_message, moderation_logs, welcome_logs FROM setupBot WHERE serverID = $1", member.guild.id)
    guild_config = dict(result) if result else None
    async with self.bot.db_pool.acquire() as connection:
    await connection.execute("DELETE FROM setup_bot WHERE server_id = $1", guild.id)  
    return prefix''' 
    
def get_intents() -> Intents:
    intents: Intents = Intents.default()
    intents.typing = False
    intents.presences = False
    intents.message_content = True
    intents.message_content = True
    return intents
def get_extensions() -> List[str]:
    ext: List[str] = []
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            ext.append(f"cogs.{filename[:-3]}")
    return ext

async def main():
    #...
    ''''async with asyncpg.create_pool(database=settings.DATABASE, user=settings.USER, 
                                        password= settings.PASSWORD, host=settings.HOST, 
                                        ssl='require', command_timeout=30) as pool:'''
    async with asyncpg.create_pool(database='postgres', user='postgres', password=settings.LOCAL_PASSWORD) as pool:
        intents = get_intents()
        exts = get_extensions()
        async with Gamigin(
            command_prefix=settings.DEFAULT_PREFIX,
            dbPool=pool,
            initialExtensions=exts,
            intents=intents,
            allowedGuilds=[settings.GAH_SERVER]
        ) as bot:
            try:
                #await bot.create_tables()
                await bot.start(settings.TOKEN)
            finally:
                await bot.dbPool.close()
                
asyncio.run(main())