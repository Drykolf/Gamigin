import asyncpg
from discord import Object
from discord.ext import commands
from typing import List, Optional
import tools.settings as settings
import cogs.queries.db_create as db
from cogs.queries.db_admin import get_guilds_data

class Zury(commands.Bot):
    def __init__(
        self,
        *args,
        initialExtensions: List[str],
        dbPool: asyncpg.Pool,
        testingGuildId: Optional[str] = settings.TEST_GUILD,
        allowedGuild: Optional[str] = settings.TEST_GUILD,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.dbPool = dbPool
        self.testingGuildId = testingGuildId
        self.initialExtensions = initialExtensions
        self.allowedGuild = allowedGuild
        self.guildData:dict = {}

    async def setup_hook(self) -> None:
        if self.dbPool is None:
            print("Connnection to database failed.")
            return
        else:
            print("Connection to database established")
        #Load commands
        for extension in self.initialExtensions:
            await self.load_extension(extension)
        if self.testingGuildId:
            guild = Object(self.testingGuildId)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f'slash commands into test server: {self.testingGuildId}')
        await self.load_guilds()
        
    async def create_tables(self) -> None:
        await db.create_dino(self.dbPool)
        await db.create_dino_capacities(self.dbPool)
        await db.create_dino_classifications(self.dbPool)
        await db.create_shiny_essences(self.dbPool)
        await db.create_player_dino(self.dbPool)
        await db.create_player_dino_capacities(self.dbPool)
        await db.create_player_dino_classifications(self.dbPool)
        await db.create_abilityrolls(self.dbPool)
        await db.create_player_bonuses(self.dbPool)
        await db.create_group_inventory(self.dbPool)
        await db.create_player_notes(self.dbPool)
        await db.create_caravan(self.dbPool)
        await db.create_eventinfo(self.dbPool)
        
    async def starting_data(self) -> None:
        import cogs.queries.db_admin as ra
        await ra.register_starting_dinos(self.dbPool)
        await ra.register_starting_capacities(self.dbPool)
        await ra.register_starting_classifications(self.dbPool)
        await ra.register_starting_abilities(self.dbPool)
        await ra.register_starting_essences(self.dbPool)
    
    async def load_guilds(self) -> None:
        result = await get_guilds_data(self.dbPool) 
        if result is None: return
        guildInfo = {}
        for data in result:
            guildInfo[data['guild_id']] = data
        self.guildData = guildInfo