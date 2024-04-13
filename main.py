import asyncio
import os
from typing import List, Optional
import asyncpg
import discord
from discord.ext import commands
import utils.settings as settings

class Gamigin(commands.Bot):
    def __init__(
        self,
        *args,
        initialExtensions: List[str],
        dbPool: asyncpg.Pool,
        testingGuildId: Optional[int] = settings.TEST_GUILD,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.dbPool = dbPool
        self.testingGuildId = testingGuildId
        self.initialExtensions = initialExtensions

    async def setup_hook(self) -> None:
        if self.dbPool is None:
            print("Connnection to database failed.")
            return
        else:
            print("Connection to database established")
        for extension in self.initialExtensions:
            await self.load_extension(extension)
        if self.testingGuildId:
            guild = discord.Object(self.testingGuildId)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            
def get_intents() -> discord.Intents:
    intents: discord.Intents = discord.Intents.default()
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
    async with asyncpg.create_pool(database=settings.DATABASE, user=settings.USER, 
                                        password= settings.PASSWORD, host=settings.HOST, 
                                        ssl='require', command_timeout=30) as pool:
        intents = get_intents()
        exts = get_extensions()
        async with Gamigin(
            command_prefix=settings.PREFIX,
            dbPool=pool,
            initialExtensions=exts,
            intents=intents,
        ) as bot:
            try:
                await bot.start(settings.TOKEN)
            finally:
                await bot.dbPool.close()
                
asyncio.run(main())