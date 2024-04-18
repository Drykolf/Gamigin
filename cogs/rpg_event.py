from discord.ext import commands, menus
from discord import Embed, Member
import schemas.rpg.user_queries as rpgDb
from utils.pagination import CapacitiesPageSource, EmbedPageSource, PlayersPageSource

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
        joiner:str = ', '
        if 'list' in args: joiner = '\n'
        result = await rpgDb.get_dinos(self.bot.dbPool)
        dinos = joiner.join(result)
        embedMsg = Embed(title="Dino list", description="List of available dinos", color=0x00ff00)
        embedMsg.add_field(name="Dinos", value=dinos, inline=False)
        await ctx.send(embed=embedMsg)
        
    @commands.command(name='classifications')
    async def show_dino_classifications(self, ctx, *args):
        '''Shows the available dino classifications from the event'''
        search = None
        if args:
            search = ' '.join(list(args)).lower()
        result = await rpgDb.get_classifications(self.bot.dbPool,search)
        embedMsg = Embed(title="Dino Classification", color=0x00ff00,
                         description="All dinos fall into one or more classifications and gain bonuses from those categories")
        for clas in result:
            info:str = f'{clas[1]} \n**Bonus:** {clas[2]}'
            embedMsg.add_field(name=clas[0],value=info, inline=False)
        await ctx.send(embed=embedMsg)

    @commands.command(name='capacities')
    async def show_dino_capacities(self, ctx, *args):
        '''Shows the available dino capacities from the event''' 
        search = None
        if args:
            search = ' '.join(list(args)).lower()
        result = await rpgDb.get_dino_capacities(self.bot.dbPool, search)
        #pagination
        pageSource = CapacitiesPageSource(result, per_page=10)
        menu = menus.MenuPages(pageSource)
        await menu.start(ctx)
        
    @commands.command(name='essences')
    async def show_shiny_essences(self, ctx, *args):
        '''Shows the available dino essences and their use in the event'''
        search = None
        if args:
            search = ' '.join(list(args)).lower()
        result = await rpgDb.get_shiny_essences(self.bot.dbPool, search)
        embedMsg = Embed(title="Shiny Dino Essences", color=0x00ff00,
                         description='''We have a mod added called shiny dinos which comes with additional buffs to all manor of dinos in the game. 
                         Here is a list of the added effects from the Campaign to these already unique dino buffs.''')
        for ess in result:
            info:str = f'{ess[1]} \n**Mastery Level:** {ess[2]}'
            embedMsg.add_field(name=ess[0],value=info, inline=False)
        await ctx.send(embed=embedMsg)
        
    @commands.command(name='abilities')
    async def show_player_info(self, ctx, *args):
        '''Shows event available ability rolls'''
        search = None
        if args:
            search = ' '.join(list(args)).lower()
        result = await rpgDb.get_ability_rolls(self.bot.dbPool, search)
        embedMsg = Embed(title="Ability Rolls", color=0x00ff00,
                         description='''These are the common type of ability checks you will make during your adventures in the campaign. 
                         Each ability has its unique function listed below and all are important.''')
        for abi in result:
            embedMsg.add_field(name=abi[0],value=abi[1], inline=False)
        await ctx.send(embed=embedMsg)
    
    @commands.command(name='bonus')
    async def show_abilities(self, ctx,ability:str, user=None):
        '''Shows player bonus in certain ability rolls'''
        #bonus hunting
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='player')
    async def show_abilities(self, ctx, *args):
        '''Shows information about the player from the event'''
        try:
            print(ctx.author.id)
            player:Member = ctx.guild.get_member(ctx.author.id)
            print(player)
        except Exception as e:
            print(e)
        await ctx.send(f'to be implemented...'+player)
        
    @commands.command(name='players')
    async def show_players(self, ctx, *args):
        '''Shows players that are participating in the event'''
        search = None
        if args:
            search = ' '.join(list(args)).lower()
        try:
            result = await rpgDb.get_players(self.bot.dbPool, search)
        except Exception as e:
            print(e)
        #pagination
        try:
            pageSource = PlayersPageSource(result, per_page=10)
            menu = menus.MenuPages(pageSource)
            await menu.start(ctx)
        except Exception as e:
            print(e)
        
async def setup(bot):
    await bot.add_cog(RPG_Event(bot))