import asyncio
import os
from typing import List
import asyncpg
from discord import Intents
import utils.settings as settings
from utils.bot import Zury

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
    print(settings.DEBUG)
    if settings.DEBUG:
        print("DEBUG MODE ON")
        pool = await asyncpg.create_pool(database='postgres', user='postgres', password=settings.LOCAL_PASSWORD)
    else:
        print("Production Mode ON")
        pool = await asyncpg.create_pool(database=settings.DATABASE, user=settings.USER, 
                                        password= settings.PASSWORD, host=settings.HOST, 
                                        ssl='require', command_timeout=30)
    intents = get_intents()
    exts = get_extensions()
    async with Zury(
        command_prefix=settings.DEFAULT_PREFIX,
        dbPool=pool,
        initialExtensions=exts,
        intents=intents,
        allowedGuild=settings.MAIN_GUILD
    ) as bot:
        try:
            await bot.create_tables()
            await bot.starting_data()
            await bot.start(settings.TOKEN)
        finally:
            await bot.dbPool.close()
    
  
asyncio.run(main())