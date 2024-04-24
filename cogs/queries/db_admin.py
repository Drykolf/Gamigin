'''ADMIN ONLY QUERIES'''
async def get_guilds_data(pool) -> list:
    async with pool.acquire() as connection:
        query = '''SELECT * FROM EventData'''
        try:
            rows = await connection.fetch(query)
            data = [dict(row.items()) for row in rows]
        except Exception as e:
            print(e)
            data = None
        return data

async def get_guild_info(pool, guildId:str) -> dict:
    async with pool.acquire() as connection:
        query = '''SELECT * FROM EventData WHERE guild_id = $1'''
        try:
            row = await connection.fetchrow(query, guildId)
            if row:data = dict(row.items())
            else: data = {}
        except Exception as e:
            print(e)
            data = None
        return data
    
async def register_guild(pool, guildId:str) -> bool:
    async with pool.acquire() as connection:
        query = '''INSERT INTO EventData (guild_id) VALUES ($1) ON CONFLICT DO NOTHING'''
        try:
            await connection.execute(query, guildId)
            return True
        except Exception as e:
            print(e)
            return False
        
async def set_guild_data(pool, guildId:str, event_channel:str=None, info_msg_id:str=None, inv_msg_id:str=None, caravan_msg_id:str=None, notes_msg_id:str=None, 
                         caravan_sslots:int=None, caravan_mslots:int=None, caravan_lslots:int=None, imprint_bonus:int=None) -> str:
    async with pool.acquire() as connection:
        query = 'UPDATE EventData SET '
        update = False
        if event_channel: 
            query += f"event_chnel_id = '{event_channel}'," 
            update=True
        if info_msg_id:
            query += f"info_msg_id = '{info_msg_id}',"
            update=True
        if inv_msg_id:
            query += f"inv_msg_id = '{inv_msg_id}',"
            update=True
        if caravan_msg_id:
            query += f"caravan_msg_id = '{caravan_msg_id}',"
            update=True
        if notes_msg_id:
            query += f"notes_msg_id = '{notes_msg_id}',"
            update=True
        if caravan_sslots:
            query += f"caravan_sslots = {caravan_sslots},"
            update=True
        if caravan_mslots:
            query += f"caravan_mslots = {caravan_mslots},"
            update=True
        if caravan_lslots:
            query += f"caravan_lslots = {caravan_lslots},"
            update=True
        if imprint_bonus:
            query += f"imprint_bonus = {imprint_bonus},"
            update=True
        if update:
            query = query[:-1] + f" WHERE guild_id = $1 RETURNING *"
            try:
                result = await connection.execute(query, guildId)
                return result
            except Exception as e:
                print(e)
                return None
        else:
            return '0'

async def register_dino_type(pool, dino_type:str) -> bool:
    async with pool.acquire() as connection:
        query = '''INSERT INTO Dinos (dino_type) 
                    VALUES ($1) ON CONFLICT (dino_type) DO NOTHING'''
        try:
            await connection.execute(query, dino_type)
            return True
        except Exception as e:
            print(f'Register Dino: {e}')
            return False

async def delete_dino_type(pool, dino_type:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM Dinos WHERE dino_type = $1 RETURNING *'''
        try:
            result = await connection.execute(query, dino_type)
            return result
        except Exception as e:
            print(e)
            return None
        
async def register_starting_dinos(pool) -> None:
    from data.initial_data import dino_types
    for dino in dino_types:
        await register_dino_type(pool, dino)
        
async def set_dino_capacity(pool, name:str, description:str) -> bool:
    async with pool.acquire() as connection:
        if description:
            query = f"""INSERT INTO DinoCapacities (name, description) VALUES ('{name}', '{description}') 
                    ON CONFLICT (name) DO UPDATE
                    SET description = '{description}'"""
        else:
            query = f"""INSERT INTO DinoCapacities (name) VALUES ('{name}') 
                    ON CONFLICT (name) DO NOTHING"""
        try:
            await connection.execute(query)
            return True
        except Exception as e:
            print(f'Set capacity: {e}')
            return False
        
async def delete_dino_capacity(pool, name:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM DinoCapacities WHERE name = $1 RETURNING *'''
        try:
            result = await connection.execute(query, name)
            return result
        except Exception as e:
            print(e)
            return None
         
async def register_starting_capacities(pool) -> None:
    from data.initial_data import dino_capacities
    for cap in dino_capacities:
        await set_dino_capacity(pool, cap[0], cap[1])
        
async def set_classification(pool, name:str, description:str, bonus:str) -> bool:
    async with pool.acquire() as connection:
        if(bonus and description):
            query = f"""INSERT INTO DinoClassifications (name, description, bonus)
                    VALUES ('{name}', '{description}', '{bonus}') ON CONFLICT (name) DO UPDATE
                    SET description = '{description}', bonus = '{bonus}'"""
        elif(description):
            query = f"""INSERT INTO DinoClassifications (name, description)
                    VALUES ('{name}', '{description}') ON CONFLICT (name) DO UPDATE
                    SET description = '{description}' """
        elif(bonus):
            query = f"""INSERT INTO DinoClassifications (name, bonus)
                    VALUES ('{name}', '{bonus}') ON CONFLICT (name) DO UPDATE
                    SET bonus = '{bonus}' """
        else:
            query = f"""INSERT INTO DinoClassifications (name)
                    VALUES ('{name}') ON CONFLICT (name) DO NOTHING"""
        try:
            await connection.execute(query)
            return True
        except Exception as e:
            print(f'Set classification {name}: {e}')
            return False
            
async def delete_classification(pool, name:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM DinoClassifications WHERE name = $1 RETURNING *'''
        try:
            result = await connection.execute(query, name)
            return result
        except Exception as e:
            print(e)
            return None
        
async def register_starting_classifications(pool) -> None:
    from data.initial_data import dino_classifications
    for clas in dino_classifications:
        await set_classification(pool, clas[0], clas[1], clas[2])
        
async def set_ability(pool, name:str, description:str) -> bool:
    async with pool.acquire() as connection:
        if(description):
            query = f"""INSERT INTO AbilityRolls (ability, description)
                    VALUES ('{name}', '{description}') ON CONFLICT (ability) DO UPDATE
                    SET description = '{description}' """
        else:
            query = f"""INSERT INTO AbilityRolls (ability)
                    VALUES ('{name}') ON CONFLICT (ability) DO NOTHING"""
        try:
            await connection.execute(query)
            await connection.execute(f'''ALTER TABLE PlayerBonus 
                                     ADD COLUMN IF NOT EXISTS {'_'.join(name.split())} smallint NOT NULL DEFAULT 0;''')
            return True
        except Exception as e:
            print(f'Set ability {name}: {e}')
            return False
        
async def delete_ability(pool, name:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM AbilityRolls WHERE ability = $1 RETURNING *'''
        try:
            result = await connection.execute(query, name)
            if result[-1] == '1':
                await connection.execute(f'''ALTER TABLE PlayerBonus 
                                     DROP COLUMN IF EXISTS {name};''')
            return result
        except Exception as e:
            print(e)
            return None

async def register_starting_abilities(pool) -> None:
    from data.initial_data import dino_abilities
    for ability in dino_abilities:
        await set_ability(pool, ability[0], ability[1])
        
async def set_essence(pool, name:str, description:str, mastery:str) -> bool:
    async with pool.acquire() as connection:
        if(description and mastery):
            query = f"""INSERT INTO ShinyEssences (shiny_name, shiny_description, shiny_mastery)
                    VALUES ('{name}', '{description}', '{mastery}') ON CONFLICT (shiny_name) DO UPDATE
                    SET shiny_description = '{description}', shiny_mastery = '{mastery}'"""
        elif(description):
            query = f"""INSERT INTO ShinyEssences (shiny_name, shiny_description)
                    VALUES ('{name}', '{description}') ON CONFLICT (shiny_name) DO UPDATE
                    SET shiny_description = '{description}'"""
        elif(mastery):
            query = f"""INSERT INTO ShinyEssences (shiny_name, shiny_mastery)
                    VALUES ('{name}', '{mastery}') ON CONFLICT (shiny_name) DO UPDATE
                    SET shiny_mastery = '{mastery}'"""
        else:
            query = f"""INSERT INTO ShinyEssences (shiny_name)
                    VALUES ('{name}') ON CONFLICT (shiny_name) DO NOTHING"""
        try:
            await connection.execute(query)
            return True
        except Exception as e:
            print(f'Set essence: {e}')
            return False
        
async def delete_essence(pool, name:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM ShinyEssences WHERE shiny_name = $1 RETURNING *'''
        try:
            result = await connection.execute(query, name)
            return result
        except Exception as e:
            print(e)
            return None
        
async def register_starting_essences(pool) -> None:
    from data.initial_data import dino_essences
    for ess in dino_essences:
        await set_essence(pool, ess[0], ess[1], ess[2])

async def register_player(pool, player_id:str,player_name:str, dino_type:str, dino_name:str) -> bool:
    async with pool.acquire() as connection:
        query = """INSERT INTO PlayerDino (user_id, user_name, dino_type, dino_name)
                    VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING"""
        try:
            await connection.execute(query, player_id, player_name, dino_type, dino_name)
            return True
        except Exception as e:
            print(e)
            return False

async def update_player_data(pool, player_id:str, dino_type:str, dino_name:str, dino_status:str, dino_personality:str, dino_shiny_essence:str, 
                     dino_imprinting:int, dino_relationship:int, companionship_lvl:int, saddle_mastery:int, dino_companionship:int, capacity:int, 
                     studious_mastery:int) -> str:
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
            query = query[:-1] + f" WHERE user_id = $1 RETURNING *"
            print(query)
            try:
                result = await connection.execute(query, player_id)
                print(result)
                return result
            except Exception as e:
                print(e)
                return None
            
async def delete_player(pool, player_id:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM PlayerDino WHERE user_id = $1 RETURNING *'''
        try:
            result = await connection.execute(query, player_id)
            return result
        except Exception as e:
            print(e)
            return None
        
async def add_class_player(pool, player_id:str, class_name:str) -> bool:
    async with pool.acquire() as connection:
        query = '''INSERT INTO PlayerDinoClassifications (user_id, classification_name) VALUES ($1, $2) ON CONFLICT DO NOTHING'''
        try:
            await connection.execute(query, player_id, class_name)
            return True
        except Exception as e:
            print(e)
            return False

async def remove_class_player(pool, player_id:str, class_name:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM PlayerDinoClassifications WHERE user_id = $1 AND classification_name = $2 RETURNING *'''
        try:
            result = await connection.execute(query, player_id, class_name)
            return result
        except Exception as e:
            print(e)
            return None

async def add_cap_player(pool, player_id:str, cap_name:str) -> bool:
    async with pool.acquire() as connection:
        query = '''INSERT INTO PlayerDinoCapacities (user_id, capacity_name) VALUES ($1, $2) ON CONFLICT DO NOTHING'''
        try:
            await connection.execute(query, player_id, cap_name)
            return True
        except Exception as e:
            print(e)
            return False
    
async def remove_cap_player(pool, player_id:str, cap_name:str) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM PlayerDinoCapacities WHERE user_id = $1 AND capacity_name = $2 RETURNING *'''
        try:
            result = await connection.execute(query, player_id, cap_name)
            return result
        except Exception as e:
            print(e)
            return None

async def set_player_bonus_roll(pool, user_id:str, ability:str, bonus:int,operator:str) -> bool:
    async with pool.acquire() as connection:
        if(operator):
            query = f'''UPDATE PlayerBonus SET {ability} = {ability} {operator} {bonus}
                        WHERE user_id = $1'''
        else:
            query = f'''UPDATE PlayerBonus SET {ability} = {bonus}
                        WHERE user_id = $1'''
        try:
            await connection.execute('''INSERT INTO PlayerBonus (user_id) VALUES ($1) ON CONFLICT DO NOTHING''', user_id)
            await connection.execute(query, user_id)
            return True
        except Exception as e:
            print(e)
            return False
            




























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
        