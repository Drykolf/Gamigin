'''CREATE TABLES FOR RPG EVENT'''
async def create_eventinfo(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                    CREATE TABLE IF NOT EXISTS EventData (
                        id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                        guild_id varchar(50) NOT NULL UNIQUE,
                        event_chnel_id varchar(50),
                        info_msg_id varchar(50),
                        inv_msg_id varchar(50),
                        caravan_msg_id varchar(50),
                        notes_msg_id varchar(50),
                        caravan_sslots int NOT NULL DEFAULT 0,
                        caravan_mslots int NOT NULL DEFAULT 0,
                        caravan_lslots int NOT NULL DEFAULT 0,
                        imprint_bonus int NOT NULL DEFAULT 0,
                        PRIMARY KEY (id)
                    )''')

async def create_dino(pool) -> None:
        async with pool.acquire() as connection:
            await connection.execute('''
                    CREATE TABLE IF NOT EXISTS Dinos(
                        id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                        dino_type varchar(50) NOT NULL UNIQUE,
                        PRIMARY KEY (id)
                    )''')


async def create_dino_classifications(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                CREATE TABLE IF NOT EXISTS DinoClassifications (
                    id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    name varchar(50) NOT NULL UNIQUE,
                    description text ,
                    bonus text,
                    PRIMARY KEY (id)
                )
            ''')

async def create_dino_capacities(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                CREATE TABLE IF NOT EXISTS DinoCapacities (
                    id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    name varchar(50) NOT NULL UNIQUE,
                    description text ,
                    PRIMARY KEY (id)
                )
            ''')

async def create_shiny_essences(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                CREATE TABLE IF NOT EXISTS ShinyEssences (
                    id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    shiny_name varchar(50) NOT NULL UNIQUE,
                    shiny_description text,
                    shiny_mastery text,
                    PRIMARY KEY (id)
                )
            ''')
        
async def create_abilityrolls(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                CREATE TABLE IF NOT EXISTS AbilityRolls (
                    id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    ability varchar(50) NOT NULL UNIQUE,
                    description text,
                    PRIMARY KEY (id)
                )
            ''')
        
async def create_player_dino(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                CREATE TABLE IF NOT EXISTS PlayerDino (
                    id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    user_id varchar(50) NOT NULL UNIQUE,
                    user_name varchar(50) NOT NULL,
                    dino_type varchar(50) NOT NULL,
                    dino_name varchar(50) NOT NULL,
                    dino_status varchar(50) NOT NULL DEFAULT 'alive',
                    dino_personality text NOT NULL DEFAULT 'Unknown',
                    dino_shiny_essence varchar(50) NOT NULL DEFAULT 'None',
                    dino_imprinting int NOT NULL DEFAULT 0,
                    dino_relationship  int NOT NULL DEFAULT 0,
                    companionship_lvl int NOT NULL DEFAULT 0,
                    saddle_mastery int NOT NULL DEFAULT 0,
                    dino_companionship int NOT NULL DEFAULT 0,
                    capacity int NOT NULL DEFAULT 0,
                    studious_mastery int NOT NULL DEFAULT 0,
                    PRIMARY KEY (id)
                )
            ''')

async def create_player_dino_classifications(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                CREATE TABLE IF NOT EXISTS PlayerDinoClassifications (
                    id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    user_id varchar(50) NOT NULL,
                    classification_name varchar(50) NOT NULL,
                    PRIMARY KEY (id)
                )
            ''')
        
async def create_player_dino_capacities(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                CREATE TABLE IF NOT EXISTS PlayerDinoCapacities (
                    id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    user_id varchar(50) NOT NULL,
                    capacity_name varchar(50) NOT NULL,
                    PRIMARY KEY (id)
                )
            ''')

async def create_player_bonuses(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS PlayerBonus (
                id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                user_id varchar(50) NOT NULL UNIQUE,
                tek smallint NOT NULL DEFAULT 0,
                geology smallint NOT NULL DEFAULT 0,
                flora_and_fauna smallint NOT NULL DEFAULT 0,
                creature_handling smallint NOT NULL DEFAULT 0,
                mystical smallint NOT NULL DEFAULT 0,
                social smallint NOT NULL DEFAULT 0,
                history smallint NOT NULL DEFAULT 0,
                insight smallint NOT NULL DEFAULT 0,
                stealth smallint NOT NULL DEFAULT 0,
                investigation smallint NOT NULL DEFAULT 0,
                perception smallint NOT NULL DEFAULT 0,
                mining smallint NOT NULL DEFAULT 0,
                herbalism smallint NOT NULL DEFAULT 0,
                fishing smallint NOT NULL DEFAULT 0,
                digging smallint NOT NULL DEFAULT 0,
                salvaging smallint NOT NULL DEFAULT 0,
                hunting smallint NOT NULL DEFAULT 0,
                scouting smallint NOT NULL DEFAULT 0,
                lock_picking smallint NOT NULL DEFAULT 0,
                dexterity smallint NOT NULL DEFAULT 0,
                companion smallint NOT NULL DEFAULT 0,
                PRIMARY KEY (id)
                )
            ''')
        
async def create_group_inventory(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS GroupInventory (
                id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                item_name varchar(50) NOT NULL UNIQUE,
                item_quantity int NOT NULL DEFAULT 1,
                item_class varchar(50) NOT NULL DEFAULT 'Generic items',
                item_category varchar(50) NOT NULL DEFAULT 'Generic material',
                PRIMARY KEY (id)
                )
            ''')

async def create_player_notes(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS PlayerNotes (
                id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                user_id varchar(50) NOT NULL,
                note text NOT NULL DEFAULT 'Blank',
                PRIMARY KEY (id)
                )
            ''')

async def create_caravan(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS Caravan (
                id int GENERATED ALWAYS AS IDENTITY NOT NULL,
                dino_type varchar(50) NOT NULL,
                dino_name varchar(50),
                dino_size int NOT NULL DEFAULT 1,
                PRIMARY KEY (id)
                )
            ''')