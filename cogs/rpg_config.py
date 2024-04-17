from discord.ext import commands
import schemas.rpg_db as db

class RPG_Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def cog_check(self, ctx) -> bool:
        if not(int(ctx.guild.id) == int(self.bot.allowedGuild) or int(ctx.guild.id) == int(self.bot.testingGuildId)):
            await ctx.send(f'Bot command only works on selected servers')
            return False
        if not ctx.permissions.manage_channels:
            await ctx.send(f'You do not have permission to use this command')
            return False
        return True
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('RPG cog is ready!')
    
    @commands.command()
    async def test(self, ctx, *args):
        '''This is a test command'''
        dino:str = ' '.join(args)
        await ctx.send(f'test {dino.capitalize()}')
    
    #todo missing argument
    @commands.command(name='regdino')
    async def register_dino(self, ctx, *args):
        '''Register a dino type to be available to be  for the event'''
        dino:str = ' '.join(args)
        async with self.bot.dbPool.acquire() as connection:
            try:
                await connection.execute('''INSERT INTO Dinos(dino_type) VALUES ($1) 
                                        ON CONFLICT(dino_type) DO NOTHING
                                        ''',dino.capitalize())
                await ctx.send(f'{dino} registered')
            except Exception as e:
                print(e)
                await ctx.send(f'Error registering {dino}')
           
async def setup(bot):
    await bot.add_cog(RPG_Config(bot))