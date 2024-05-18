
async def add_note(pool, user_id: str, note: str) -> bool:
    async with pool.acquire() as connection:
        query = '''INSERT INTO PlayerNotes (user_id, note) VALUES ($1, $2)'''
        try:
            await connection.execute(query, user_id, note)
            return True
        except Exception as e:
            print(e)
            return False

async def delete_note(pool, id:int) -> str:
    async with pool.acquire() as connection:
        query = '''DELETE FROM PlayerNotes WHERE id = $1 RETURNING *'''
        try:
            result = await connection.execute(query, id)
            return result
        except Exception as e:
            print(e)
            return None

async def get_notes(pool) -> list:
    async with pool.acquire() as connection:
        query = '''SELECT id, note FROM PlayerNotes'''
        try:
            rows = await connection.fetch(query)
            data = [list(row.values()) for row in rows]
        except Exception as e:
            print(e)
            data = None
        return data
    
async def get_dinos(pool) -> list:
    async with pool.acquire() as connection:
        try:
            rows = await connection.fetch('''
            SELECT * FROM Dinos ORDER BY dino_type ASC 
            ''')
            data = [list(row.values())[1] for row in rows] #Returns a list of all the dino_type values
            return data
        except Exception as e:
            print(e)
            return None
    
async def get_classifications(pool, name=None) -> list:
    async with pool.acquire() as connection:
        if not name:query = '''SELECT * FROM DinoClassifications ORDER BY name ASC'''
        else: query = f'''SELECT * FROM DinoClassifications WHERE LOWER(name) LIKE '%{name}%' ORDER BY name ASC'''
        try: 
            rows = await connection.fetch(query)
            data = [list(row.values())[1:] for row in rows] #Returns a list of all the dino_type values
        except Exception as e:
            print(e)
            data = None
        return data
    
async def get_shiny_essences(pool, name=None) -> list:
    async with pool.acquire() as connection:
        if not name: query = f'''SELECT * FROM ShinyEssences ORDER BY shiny_name ASC'''
        else: query =f'''SELECT * FROM ShinyEssences WHERE LOWER(shiny_name) LIKE '%{name}%' ORDER BY shiny_name ASC'''
        try:
            rows = await connection.fetch(query)
            data = [list(row.values())[1:] for row in rows] #Returns a list of all the essences values
        except Exception as e:
            print(e)
            data = None
        return data
    
async def get_ability_rolls(pool, name=None) -> list:
    async with pool.acquire() as connection:
        if not name: query = '''SELECT * FROM AbilityRolls ORDER BY ability ASC'''
        else: query = f'''SELECT * FROM AbilityRolls WHERE LOWER(ability) LIKE '%{name}%' ORDER BY ability ASC'''
        try:
            rows = await connection.fetch(query)
            data = [list(row.values())[1:] for row in rows] #Returns a list of all the ability values
        except Exception as e:
            print(e)
            data = None
        return data

async def get_dino_capacities(pool, name: str=None) -> list:
    async with pool.acquire() as connection:
        if not name: query = '''SELECT name, description FROM DinoCapacities ORDER BY name'''
        else: query = f'''SELECT name, description FROM DinoCapacities WHERE LOWER(name) LIKE '%{name}%' ORDER BY name'''
        try:
            rows = await connection.fetch(query)
            data = [list(row.values()) for row in rows] #Returns a list of all the dino_type values
        except Exception as e:
            print(e)
            data = None
        return data
    
async def get_players(pool, arg: str=None) -> list:
    async with pool.acquire() as connection:
        if not arg: query = '''SELECT user_name, dino_type, dino_name FROM PlayerDino ORDER BY user_name'''
        else: query =f'''
                SELECT user_name, dino_type, dino_name FROM PlayerDino 
                WHERE LOWER(user_name) LIKE '%{arg}%' 
                OR LOWER(dino_type) LIKE '%{arg}%'
                OR LOWER(dino_name) LIKE '%{arg}%'
                ORDER BY user_name
                '''
        try:
            rows = await connection.fetch(query)
            data = [list(row.values()) for row in rows] #Returns a list of all the players
        except Exception as e:
            print(e)
            data = None
        return data

async def get_player_info(pool, player: str) -> list:
    async with pool.acquire() as connection:
        query = '''SELECT * FROM PlayerDino WHERE user_id = $1'''
        try:
            row = await connection.fetchrow(query, player)
            if row:data = dict(row.items())
            else: data = []
        except Exception as e:
            print(e)
            data = None
        return data

async def get_player_classifications(pool, player: str) -> list:
    async with pool.acquire() as connection:
        query = '''SELECT classification_name FROM PlayerDinoClassifications WHERE user_id = $1'''
        try:
            rows = await connection.fetch(query, player)
            data = [list(row.values())[0] for row in rows]
        except Exception as e:
            print(e)
            data = None
        return data

async def get_player_capacities(pool, player: str) -> list:
    async with pool.acquire() as connection:
        query = '''SELECT capacity_name FROM PlayerDinoCapacities WHERE user_id = $1'''
        try: 
            rows = await connection.fetch(query, player)
            data = [list(row.values())[0] for row in rows]
        except Exception as e:
            print(e)
            data = None
        return data
    
async def get_player_absbonuses(pool, player:str) -> list:
    async with pool.acquire() as connection:
        query = '''SELECT * FROM PlayerBonus WHERE user_id = $1 '''
        try:
            row = await connection.fetchrow(query, player)
            data = []
            if row:
                info = list(row.items())[2:]
                for r in info:
                    data.append((r[0].replace('_',' '),r[1]))
        except Exception as e:
            print(e)
            data = None
        return data
    
async def get_inventory(pool) -> list:
    async with pool.acquire() as connection:
        query = '''SELECT * FROM GroupInventory'''
        try:
            rows = await connection.fetch(query)
            data = [list(row.values()) for row in rows]
        except Exception as e:
            print(e)
            data = None
        return data
    