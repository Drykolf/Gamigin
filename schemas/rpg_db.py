async def create_dino_datatable(pool) -> None:
        async with pool.acquire() as connection:
            await connection.execute("""
                    CREATE TABLE IF NOT EXISTS "Dinos" (
                        "id" int GENERATED ALWAYS AS IDENTITY NOT NULL,
                        "dino_type" text NOT NULL,
                        PRIMARY KEY ("id")
                    )""")

async def create_dino_classifications_datatable(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("""
                CREATE TABLE IF NOT EXISTS "DinoClassifications" (
                    "id" int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    "name" text NOT NULL,
                    "description" text NOT NULL,
                    "bonus" text NOT NULL,
                    PRIMARY KEY ("id")
                )
            """)

async def create_dino_capacities_datatable(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("""
                CREATE TABLE IF NOT EXISTS "DinoCapacities" (
                    "id" int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    "name" text NOT NULL,
                    "description" text NOT NULL,
                    PRIMARY KEY ("id")
                )
            """)
        
async def create_player_dino_datatable(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("""
                CREATE TABLE IF NOT EXISTS "PlayerDino" (
                    "user_id" int NOT NULL UNIQUE,
                    "dino_type" int NOT NULL,
                    "dino_name" text NOT NULL,
                    "dino_personality" text NOT NULL,
                    "dino_shiny_essence" int NOT NULL,
                    "dino_imprinting" int NOT NULL DEFAULT '0',
                    "dino_relationship " int NOT NULL DEFAULT '0',
                    "companionship_lvl" int NOT NULL DEFAULT '0',
                    "saddle_mastery" int NOT NULL DEFAULT '0',
                    "dino_companionship" int NOT NULL DEFAULT '0',
                    "capacity" int NOT NULL DEFAULT '0',
                    "studious_mastery" int NOT NULL DEFAULT '0',
                    PRIMARY KEY ("user_id")
                )
            """)

async def create_player_dino_classifications_datatable(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("""
                CREATE TABLE IF NOT EXISTS "PlayerDinoClassifications" (
                    "id" int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    "user_id" int NOT NULL,
                    "classification_id" int NOT NULL,
                    PRIMARY KEY ("id")
                )
            """)
        
async def create_player_dino_capacities_datatable(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("""
                CREATE TABLE IF NOT EXISTS "PlayerDinoCapacities" (
                    "id" int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    "user_id" int NOT NULL,
                    "capacity_id" int NOT NULL,
                    PRIMARY KEY ("id")
                )
            """)

async def create_shiny_essences_datatable(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("""
                CREATE TABLE IF NOT EXISTS "ShinyEssences" (
                    "id" int GENERATED ALWAYS AS IDENTITY NOT NULL,
                    "shiny_name" text NOT NULL,
                    "shiny_description" text NOT NULL,
                    PRIMARY KEY ("id")
                )
            """)

async def add_constraints(pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("""
                            ALTER TABLE "PlayerDino" ADD CONSTRAINT "PlayerDino_fk1" FOREIGN KEY ("dino_type") REFERENCES "Dinos"("id");
                            ALTER TABLE "PlayerDino" ADD CONSTRAINT "PlayerDino_fk4" FOREIGN KEY ("dino_shiny_essence") REFERENCES "ShinyEssences"("id");
                            ALTER TABLE "PlayerDinoClassifications" ADD CONSTRAINT "PlayerDinoClassifications_fk1" FOREIGN KEY ("user_id") REFERENCES "PlayerDino"("user_id");
                            ALTER TABLE "PlayerDinoClassifications" ADD CONSTRAINT "PlayerDinoClassifications_fk2" FOREIGN KEY ("classification_id") REFERENCES "DinoClassifications"("id");
                            ALTER TABLE "PlayerDinoCapacities" ADD CONSTRAINT "PlayerDinoCapacities_fk1" FOREIGN KEY ("user_id") REFERENCES "PlayerDino"("user_id");
                            ALTER TABLE "PlayerDinoCapacities" ADD CONSTRAINT "PlayerDinoCapacities_fk2" FOREIGN KEY ("capacity_id") REFERENCES "DinoCapacities"("id");
                             """)