'''INSERT INTO TABLES'''
async def register_dino_type(pool, dino_type) -> None:
    async with pool.acquire() as connection:
        await connection.execute('''INSERT INTO Dinos (dino_type) 
                                    VALUES ($1) 
                                    ''', dino_type)
        row = await connection.fetchrow('SELECT * FROM Dinos WHERE dino_type = $1', dino_type)
        print(f'Registered {row}')