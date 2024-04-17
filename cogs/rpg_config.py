from discord.ext import commands

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
        print('RPG config cog is ready!')
    
    @commands.command()
    async def testadmin(self, ctx, *args):
        '''This is a test command'''
        test:str = ' '.join(args)
        await ctx.send(f'test {test.capitalize()}')
    
    #todo missing argument
    @commands.command(name='regdino')
    async def register_dino(self, ctx, *args):
        '''Register a dino type to be available to be available for the event'''
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
                
    @commands.command(name='deldino')
    async def delete_dino(self, ctx, *args):
        '''Delete a dino type from the list for the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='regclass')
    async def register_class(self, ctx, *args):
        '''Register class'''
        clas:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='delclass')
    async def delete_class(self, ctx, *args):
        '''Delete class'''
        clas:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='regcap')
    async def register_capacity(self, ctx, *args):
        '''Register capacity'''
        cap:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='delcap')
    async def delete_capacity(self, ctx, *args):
        '''Delete capacity'''
        cap:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='regess')
    async def register_essence(self, ctx, *args):
        '''Register shiny essence'''
        ess:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='deless')
    async def delete_essence(self, ctx, *args):
        '''Delete shiny essence'''
        ess:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='regplayer')
    async def register_player(self, ctx, *args):
        '''Register event player'''
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='delplayer')
    async def register_player(self, ctx, *args):
        '''Delete event player'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='edtplayer')
    async def edit_player(self, ctx, *args):
        '''Modify event player'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='addplayerclass')
    async def add_player_classification(self, ctx, *args):
        '''Add player dino classification'''
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='delplayerclass')
    async def delete_player_classification(self, ctx, *args):
        '''Delete player dino classification'''
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='addplayercap')
    async def add_player_capacity(self, ctx, *args):
        '''Add player dino capacity'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='delplayercap')
    async def delete_player_capacity(self, ctx, *args):
        '''Delete player dino capacity'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='regability')
    async def register_abilityroll(self, ctx, *args):
        '''Register ability roll'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='delability')
    async def Delete_abilityroll(self, ctx, *args):
        '''Delete ability roll'''
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='addbonus')
    async def add_player_ability_bonus(self, ctx, *args):
        '''Add player ability roll bonus'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='delbonus')
    async def add_player_ability_bonus(self, ctx, *args):
        '''Delete player ability roll bonus'''
        await ctx.send(f'to be implemented...')
           
async def setup(bot):
    await bot.add_cog(RPG_Config(bot))