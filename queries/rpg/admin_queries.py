'''INSERT INTO TABLES'''
from turtle import update


async def register_dino_type(pool, dino_type) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''INSERT INTO Dinos (dino_type) 
                                    VALUES ($1) ON CONFLICT (dino_type) DO NOTHING
                                    ''', dino_type)
        
async def register_starting_dinos(pool) -> None:
    from data.initial_data import dino_types
    for dino in dino_types:
        await register_dino_type(pool, dino)
        
async def register_dino_capacity(pool, name, description):
    async with pool.acquire() as connection:
        if description:
            await connection.execute('''
                INSERT INTO DinoCapacities (name, description) VALUES ($1, $2) 
                ON CONFLICT (name) DO UPDATE
                SET description = $2
            ''', name, description)
        else:
            await connection.execute('''
                INSERT INTO DinoCapacities (name) VALUES ($1) 
                ON CONFLICT (name) DO NOTHING
            ''', name)
        
async def register_starting_capacities(pool) -> None:
    from data.initial_data import dino_capacities
    for cap in dino_capacities:
        await register_dino_capacity(pool, cap[0], cap[1])
        
async def register_classification(pool, name, description, bonus):
    async with pool.acquire() as connection:
        if(bonus and description):
            await connection.execute('''
                INSERT INTO DinoClassifications (name, description, bonus)
                VALUES ($1, $2, $3) ON CONFLICT (name) DO UPDATE
                SET description = $2, bonus = $3
            ''', name, description, bonus)
        elif(description):
            await connection.execute('''
                INSERT INTO DinoClassifications (name, description)
                VALUES ($1, $2) ON CONFLICT (name) DO UPDATE
                SET description = $2
            ''', name, description)
        elif(bonus):
            await connection.execute('''
                INSERT INTO DinoClassifications (name, bonus)
                VALUES ($1, $2) ON CONFLICT (name) DO UPDATE
                SET bonus = $2
            ''', name, bonus)
        else:
            await connection.execute('''
                INSERT INTO DinoClassifications (name)
                VALUES ($1) ON CONFLICT (name) DO NOTHING
            ''', name)
        
async def register_starting_classifications(pool) -> None:
    from data.initial_data import dino_classifications
    for clas in dino_classifications:
        await register_classification(pool, clas[0], clas[1], clas[2])
        
async def register_ability(pool, name, description):
    async with pool.acquire() as connection:
        if(description):
            await connection.execute('''
                INSERT INTO AbilityRolls (ability, description)
                VALUES ($1, $2) ON CONFLICT (ability) DO UPDATE
                SET description = $2
            ''', name, description)
        else:
            await connection.execute('''
                INSERT INTO AbilityRolls (ability)
                VALUES ($1) ON CONFLICT (ability) DO NOTHING
            ''', name)
        await connection.execute(f'''ALTER TABLE PlayerBonus 
                                     ADD COLUMN IF NOT EXISTS {name} smallint NOT NULL DEFAULT 0;''')
        
async def register_starting_abilities(pool) -> None:
    from data.initial_data import dino_abilities
    for ability in dino_abilities:
        await register_ability(pool, ability[0], ability[1])
        
async def register_essence(pool, name, description, mastery):
    async with pool.acquire() as connection:
        if(description and mastery):
            await connection.execute('''
                INSERT INTO ShinyEssences (shiny_name, shiny_description, shiny_mastery)
                VALUES ($1, $2, $3) ON CONFLICT (shiny_name) DO UPDATE
                SET shiny_description = $2, shiny_mastery = $3
            ''', name, description, mastery)
        elif(description):
            await connection.execute('''
                INSERT INTO ShinyEssences (shiny_name, shiny_description)
                VALUES ($1, $2) ON CONFLICT (shiny_name) DO UPDATE
                SET shiny_description = $2
            ''', name, description)
        elif(mastery):
            await connection.execute('''
                INSERT INTO ShinyEssences (shiny_name, shiny_mastery)
                VALUES ($1, $2) ON CONFLICT (shiny_name) DO UPDATE
                SET shiny_mastery = $2
            ''', name, mastery)
        else:
            await connection.execute('''
                INSERT INTO ShinyEssences (shiny_name)
                VALUES ($1) ON CONFLICT (shiny_name) DO NOTHING
            ''', name)
        
async def register_starting_essences(pool) -> None:
    from data.initial_data import dino_essences
    for ess in dino_essences:
        await register_essence(pool, ess[0], ess[1], ess[2])

async def set_player_bonus_roll(pool, user_id:str, ability:str, bonus:int,operator:str):
    async with pool.acquire() as connection:
        await connection.execute('''INSERT INTO PlayerBonus (user_id) VALUES ($1) ON CONFLICT DO NOTHING''', user_id)
        if(operator):
            await connection.execute(f'''
                UPDATE PlayerBonus SET {ability} = {ability} {operator} {bonus}
                WHERE user_id = $1
            ''', user_id)
        else:
            await connection.execute(f'''
                UPDATE PlayerBonus SET {ability} = {bonus}
                WHERE user_id = $1
            ''', user_id)
            
async def register_player(pool, player_id:str,player_name:str, dino_type:str, dino_name:str):
    async with pool.acquire() as connection:
        await connection.execute('''INSERT INTO PlayerDino (user_id, user_name, dino_type, dino_name)
                                    VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING''', player_id, player_name, dino_type, dino_name)

async def set_player_data(pool, player_id:str, dino_type:str, dino_name:str, dino_status:str, dino_personality:str, dino_shiny_essence:str, 
                     dino_imprinting:int, dino_relationship:int, companionship_lvl:int, saddle_mastery:int, dino_companionship:int, capacity:int, studious_mastery:int):
    async with pool.acquire() as connection:
        query = 'UPDATE PlayerDino SET '
        update = False
        if dino_type: 
            query += f"dino_type = '{dino_type}'," 
            update=True
        if dino_name: 
            query += f"dino_name = '{dino_name}',"
            update=True
        if dino_status: 
            query += f"dino_status = '{dino_status}',"
            update=True
        if dino_personality: 
            query += f"dino_personality = '{dino_personality}',"
            update=True
        if dino_shiny_essence: 
            query += f"dino_shiny_essence = '{dino_shiny_essence}',"
            update=True
        if dino_imprinting: 
            query += f"dino_imprinting = {dino_imprinting},"
            update=True
        if dino_relationship: 
            query += f"dino_relationship = {dino_relationship},"
            update=True
        if companionship_lvl: 
            query += f"companionship_lvl = {companionship_lvl},"
            update=True
        if saddle_mastery: 
            query += f"saddle_mastery = {saddle_mastery},"
            update=True
        if dino_companionship: 
            query += f"dino_companionship = {dino_companionship},"
            update=True
        if capacity: 
            query += f"capacity = {capacity},"
            update=True
        if studious_mastery: 
            query += f"studious_mastery = {studious_mastery},"
            update=True
        if update:
            query = query[:-1] + f" WHERE user_id = $1"
            print(query)
            await connection.execute(query, player_id)



























'''Group item inventory'''
async def set_item(pool, item_name, item_class=None, item_cat=None, item_quantity= None) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''
                            INSERT INTO GroupInventory(item_name)
                            VALUES ($1) ON CONFLICT DO NOTHING''', item_name)
        query = ''
        update = False
        if(item_class):
            query += f'item_class = {item_class},'
            update = True
        if(item_cat):
            query += f'item_category = {item_cat},'
            update = True
        if(item_quantity):
            query += f'item_quantity = {item_quantity},'
            update = True
        if update: await connection.execute('''UPDATE GroupInventory SET '''+query[:-1])
        