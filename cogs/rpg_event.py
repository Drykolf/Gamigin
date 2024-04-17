from discord.ext import commands
class RPG_Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx) -> bool:
        if not(int(ctx.guild.id) == int(self.bot.allowedGuild) or int(ctx.guild.id) == int(self.bot.testingGuildId)):
            await ctx.send(f'Bot command only works on selected servers')
            return False
        return True
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('RPG cog is ready!')

    @commands.command()
    async def test(self, ctx, *args):
        '''This is a test command'''
        test:str = ' '.join(args)
        await ctx.send(f'test {test.capitalize()}')
        
    @commands.command(name='dinos')
    async def show_dino_types(self, ctx, *args):
        '''Shows the available dinos to be chosen from, for the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='classifications')
    async def show_dino_classifications(self, ctx, *args):
        '''Shows the available dino classifications from the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')

    @commands.command(name='capacities')
    async def show_dino_capacities(self, ctx, *args):
        '''Shows the available dino capacities from the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='essences')
    async def show_shiny_essences(self, ctx, *args):
        '''Shows the available dino essences and their use in the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='players')
    async def show_players(self, ctx, *args):
        '''Shows players that are participating in the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='player')
    async def show_player_info(self, ctx, *args):
        '''Shows information about the player from the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='abilities')
    async def show_abilities(self, ctx, *args):
        '''Shows event available ability rolls'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='bonus')
    async def show_abilities(self, ctx,ability:str, user=None):
        '''Shows player bonus in certain ability rolls'''
        await ctx.send(f'to be implemented...')
        
async def setup(bot):
    await bot.add_cog(RPG_Event(bot))