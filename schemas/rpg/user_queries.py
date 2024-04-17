
async def get_dinos(pool) -> list:
    async with pool.acquire() as connection:
        rows = await connection.fetch('''
        SELECT * FROM Dinos ORDER BY dino_type ASC 
        ''')
        data = [list(row.values())[1] for row in rows] #Returns a list of all the dino_type values
        return data
    
async def get_classifications(pool, param=None) -> list:
    async with pool.acquire() as connection:
        if not param:
            rows = await connection.fetch('''
            SELECT * FROM DinoClassifications ORDER BY name ASC
            ''')
        else:
            try:
                rows = await connection.fetch(f'''
                SELECT * FROM DinoClassifications WHERE LOWER(name) LIKE '%{param}%' ORDER BY name ASC
                ''')
            except Exception as e:
                print(e)
        data = [list(row.values())[1:] for row in rows] #Returns a list of all the dino_type values
        return data