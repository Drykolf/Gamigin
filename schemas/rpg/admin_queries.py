'''INSERT INTO TABLES'''
async def register_dino_type(pool, dino_type) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''INSERT INTO Dinos (dino_type) 
                                    VALUES ($1) ON CONFLICT (dino_type) DO NOTHING
                                    ''', dino_type)
        print(f'Registered {dino_type}')
        
async def register_starting_dinos(pool) -> None:
    from utils.extras import dino_types
    for dino in dino_types:
        await register_dino_type(pool, dino)
        
async def register_dino_capacity(pool, name, description):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO DinoCapacities (name, description) VALUES ($1, $2) 
            ON CONFLICT (name) DO UPDATE
            SET description = $2
        ''', name, description)
        
async def register_starting_capacities(pool) -> None:
    from utils.extras import dino_capacities
    for cap in dino_capacities:
        await register_dino_capacity(pool, cap[0], cap[1])
        
async def register_classification(pool, name, description, bonus):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO DinoClassifications (name, description, bonus)
            VALUES ($1, $2, $3) ON CONFLICT (name) DO UPDATE
            SET description = $2, bonus = $3
        ''', name, description, bonus)
        
async def register_starting_classifications(pool) -> None:
    from utils.extras import dino_classifications
    for clas in dino_classifications:
        await register_classification(pool, clas[0], clas[1], clas[2])
        
async def register_ability(pool, name, description):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO AbilityRolls (ability, description)
            VALUES ($1, $2) ON CONFLICT (ability) DO UPDATE
            SET description = $2
        ''', name, description)
        
async def register_starting_abilities(pool) -> None:
    from utils.extras import dino_abilities
    for ability in dino_abilities:
        await register_ability(pool, ability[0], ability[1])
        
async def register_essence(pool, name, description, mastery):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO ShinyEssences (shiny_name, shiny_description, shiny_mastery)
            VALUES ($1, $2, $3) ON CONFLICT (shiny_name) DO UPDATE
            SET shiny_description = $2, shiny_mastery = $3
        ''', name, description, mastery)
        
async def register_starting_essences(pool) -> None:
    from utils.extras import dino_essences
    for ess in dino_essences:
        await register_essence(pool, ess[0], ess[1], ess[2])