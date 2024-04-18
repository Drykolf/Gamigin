
async def get_dinos(pool) -> list:
    async with pool.acquire() as connection:
        rows = await connection.fetch('''
        SELECT * FROM Dinos ORDER BY dino_type ASC 
        ''')
        data = [list(row.values())[1] for row in rows] #Returns a list of all the dino_type values
        return data
    
async def get_classifications(pool, name=None) -> list:
    async with pool.acquire() as connection:
        if not name:
            rows = await connection.fetch('''
            SELECT * FROM DinoClassifications ORDER BY name ASC
            ''')
        else:
            rows = await connection.fetch(f'''
                SELECT * FROM DinoClassifications WHERE LOWER(name) LIKE '%{name}%' ORDER BY name ASC
                ''')
        data = [list(row.values())[1:] for row in rows] #Returns a list of all the dino_type values
        return data
    
async def get_shiny_essences(pool, name=None) -> list:
    async with pool.acquire() as connection:
        if not name:
            rows = await connection.fetch('''
                SELECT * FROM ShinyEssences ORDER BY shiny_name ASC
                ''')
        else:
            rows = await connection.fetch(f'''
                SELECT * FROM ShinyEssences WHERE LOWER(shiny_name) LIKE '%{name}%' ORDER BY shiny_name ASC
                ''')
        data = [list(row.values())[1:] for row in rows] #Returns a list of all the dino_type values
        return data
    
async def get_ability_rolls(pool, name=None) -> list:
    async with pool.acquire() as connection:
        if not name:
            rows = await connection.fetch('''
                SELECT * FROM AbilityRolls ORDER BY ability ASC
                ''')
        else: 
            rows = await connection.fetch(f'''
                SELECT * FROM AbilityRolls WHERE LOWER(ability) LIKE '%{name}%' ORDER BY ability ASC
                ''')
        data = [list(row.values())[1:] for row in rows] #Returns a list of all the dino_type values
        return data

async def get_dino_capacities(pool, name: str=None) -> list:
    async with pool.acquire() as connection:
        if not name:
            rows = await connection.fetch('''
                SELECT name, description FROM DinoCapacities ORDER BY name
                ''')
        else:
            rows = await connection.fetch(f'''
                SELECT name, description FROM DinoCapacities WHERE LOWER(name) LIKE '%{name}%' ORDER BY name
                ''')
        data = [list(row.values()) for row in rows] #Returns a list of all the dino_type values
        return data
    
async def get_players(pool, arg: str=None) -> list:
    async with pool.acquire() as connection:
        if not arg:
            rows = await connection.fetch('''
                SELECT user_name, dino_type, dino_name FROM PlayerDino ORDER BY user_name
                ''')
        else:
            rows = await connection.fetch(f'''
                SELECT user_name, dino_type, dino_name FROM PlayerDino 
                WHERE LOWER(user_name) LIKE '%{arg}%' 
                OR LOWER(dino_type) LIKE '%{arg}%'
                OR LOWER(dino_name) LIKE '%{arg}%'
                ORDER BY user_name
                ''')
        data = [list(row.values()) for row in rows] #Returns a list of all the dino_type values
        return data