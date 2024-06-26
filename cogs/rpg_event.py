from tkinter import E
from typing import Optional
from discord.ext import commands, menus
from discord.ext.commands import Context
from discord import Embed, Member, NotFound
import cogs.queries.db_user as rpgDb
from cogs.queries.db_admin import set_guild_data
from cogs.utils.paginator import CapacitiesPageSource, PlayersPageSource

class RPG_Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx) -> bool:
        if not(int(ctx.guild.id) == int(self.bot.allowedGuild) or int(ctx.guild.id) == int(self.bot.testingGuildId)):
            await ctx.send(f'Bot command only works on selected servers')
            return False
        return True
    
    def formatInventory(self, items):
        embedMsg = Embed(title='Group Inventory', description='Everything the group has collected:')
        itemClasses = []
        for item in items:
            if item[3] not in itemClasses:
                itemClasses.append(item[3])
        for clas in itemClasses:
            itemCategories = []
            content = ''
            embedMsg.add_field(name=clas.upper(), value='\u200b', inline=True)
            for item in items:
                if item[3] == clas:
                    if item[4] not in itemCategories:
                        itemCategories.append(item[4])
            for cat in itemCategories:
                content += f'**{cat}**\n'
                for item in items:
                    if item[3] == clas and item[4] == cat:
                        content += f'{item[1]}: x{item[2]}\n'
            embedMsg.add_field(name='\u200b',value=content, inline=True)
            embedMsg.add_field(name='\u200b', value='\u200b', inline=True)
        return embedMsg
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('RPG cog is ready!')

    async def update_notes_msg(self,ctx:Context) -> None:
        if (str(ctx.guild.id) in self.bot.guildData):
            data = self.bot.guildData[str(ctx.guild.id)]
            if (data['event_chnel_id']!=None and data['event_chnel_id'] != '0'):
                channel = ctx.guild.get_channel(int(data['event_chnel_id']))
                match data['notes_msg_id']:
                    case None: return
                    case '0': return
                    case '1': 
                        msg = await channel.send(content='No notes added yet...')
                        await set_guild_data(self.bot.dbPool, str(ctx.guild.id), notes_msg_id=str(msg.id))
                        data['notes_msg_id'] = str(msg.id)
                        await self.bot.load_guilds()
                try:
                    notesMsg = channel.get_partial_message(int(data['notes_msg_id']))
                    if (notes := await rpgDb.get_notes(self.bot.dbPool)) is not None:
                        notesContent = '\n'.join([f'{note[0]}: {note[1]}' for note in notes])
                        notesContent = '**Notes:** \n'+notesContent
                        await notesMsg.edit(content=notesContent)
                    else:
                        await notesMsg.edit(content='No notes added yet...')
                except NotFound as e:
                    await set_guild_data(self.bot.dbPool, str(ctx.guild.id), notes_msg_id='0')
                    data['notes_msg_id'] = '0'
                    await self.bot.load_guilds()
                except Exception as e:
                    print(e)
                    #log error
                
    @commands.hybrid_command()
    async def prueba(self, ctx, *, args: Optional[str] = None):
        '''This is a test command'''
        test = 'hola'
        print(self.bot.guildData)
        if args: test = args
        await ctx.send(f'test {test.capitalize()}')
        
    @commands.hybrid_command(name='note', aliases=['n'])
    async def add_note(self, ctx: Context, *, note: str):
        '''Adds a note for the group'''
        await ctx.defer()
        note = note.replace('\'', '\'\'')
        result = await rpgDb.add_note(self.bot.dbPool, str(ctx.author.id), note)
        if result:
            await ctx.send('Note added')
            await self.update_notes_msg(ctx)
        else:
            await ctx.send('Error adding note')
            
    @commands.hybrid_command(name='delnote', aliases=['dn'])
    async def del_note(self, ctx: Context, id:int):
        '''Deletes a note'''
        await ctx.defer()
        result = await rpgDb.delete_note(self.bot.dbPool, id)
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = 'Error: note not found'
            else: 
                msg = 'Note deleted'
                await self.update_notes_msg(ctx)
        else: msg = 'Error deleting note'
        await ctx.send(msg)
    
    @commands.hybrid_command(name='notes', aliases=['ns'])
    async def show_notes(self, ctx: Context):
        '''Shows the group notes'''
        result = await rpgDb.get_notes(self.bot.dbPool)
        if result is None:
            await ctx.send('Error fetching notes')
            return
        notes = '\n'.join([f'{note[0]}: {note[1]}' for note in result])
        embedMsg = Embed(title='Group Notes', description=notes)
        await ctx.send(embed=embedMsg)
        
    @commands.hybrid_command(name='dinos')
    async def show_dino_types(self, ctx: Context, *, args: Optional[str] = ''):
        '''Shows the available dinos to be chosen from'''
        joiner:str = ', '
        if 'list' in args: joiner = '\n'
        result = await rpgDb.get_dinos(self.bot.dbPool)
        if result is None:
            await ctx.send('Error fetching dinos')
            return
        dinos = joiner.join(result)
        embedMsg = Embed(title="Dino list", description="List of available dinos", color=0x00ff00)
        embedMsg.add_field(name="Dinos", value=dinos, inline=False)
        await ctx.send(embed=embedMsg)
        
    @commands.hybrid_command(name='classifications', aliases=['class'])
    async def show_dino_classifications(self, ctx: Context, *, args: Optional[str] = None):
        '''Shows the available dino classifications'''
        search = None
        if args:
            search = args.lower()
        result = await rpgDb.get_classifications(self.bot.dbPool,search)
        if result is None:
            await ctx.send('Error fetching classifications')
            return
        embedMsg = Embed(title="Dino Classification", color=0x00ff00,
                         description="All dinos fall into one or more classifications and gain bonuses from those categories")
        for clas in result:
            info:str = f'{clas[1]} \n**Bonus:** {clas[2]}'
            embedMsg.add_field(name=clas[0],value=info, inline=False)
        await ctx.send(embed=embedMsg)

    @commands.hybrid_command(name='capacities', aliases=['caps'])
    async def show_dino_capacities(self, ctx: Context, *, args: Optional[str] = None):
        '''Shows the available dino capacities''' 
        search = None
        if args:
            search = args.lower()
        result = await rpgDb.get_dino_capacities(self.bot.dbPool, search)
        if result is None:
            await ctx.send('Error fetching capacities')
            return
        #pagination
        pageSource = CapacitiesPageSource(result, per_page=10)
        menu = menus.MenuPages(pageSource)
        await ctx.send('Capacities: ', ephemeral=True)
        await menu.start(ctx)
        
        
    @commands.hybrid_command(name='essences', aliases=['ess'])
    async def show_shiny_essences(self, ctx: Context, *, args: Optional[str] = None):
        '''Shows the available dino essences and their use'''
        search = None
        if args:
            search = args.lower()
        result = await rpgDb.get_shiny_essences(self.bot.dbPool, search)
        if result is None:
            await ctx.send('Error fetching essences')
            return
        embedMsg = Embed(title="Shiny Dino Essences", color=0x00ff00,
                         description='''We have a mod added called shiny dinos which comes with additional buffs to all manor of dinos in the game. 
                         Here is a list of the added effects from the Campaign to these already unique dino buffs.''')
        for ess in result:
            info:str = f'{ess[1]} \n**Mastery Level:** {ess[2]}'
            embedMsg.add_field(name=ess[0],value=info, inline=False)
        await ctx.send(embed=embedMsg)
        
    @commands.hybrid_command(name='abilities', aliases=['abs'])
    async def show_player_info(self, ctx: Context, *, args: Optional[str] = None):
        '''Shows event available ability rolls'''
        search = None
        if args:
            search = args.lower()
        result = await rpgDb.get_ability_rolls(self.bot.dbPool, search)
        if result is None:
            await ctx.send('Error fetching abilities')
            return
        embedMsg = Embed(title="Ability Rolls", color=0x00ff00,
                         description='''These are the common type of ability checks you will make during your adventures in the campaign. 
                         Each ability has its unique function listed below and all are important.''')
        for abi in result:
            embedMsg.add_field(name=abi[0],value=abi[1], inline=False)
        await ctx.send(embed=embedMsg)
    
    @commands.hybrid_command(name='bonus', aliases=['b'])
    async def show_bonuses(self, ctx: Context, *, search: Optional[str] = None, player: Optional[Member] = None):
        '''Shows player bonus in certain ability rolls'''
        if search and not player:
            search = search.lower()
            try:
                p = search.split()[-1]
                player = ctx.guild.get_member(int(p[2:-1]))
                search = search[:-len(p)-1]
            except:
                player = ctx.author
        if not player:
            player = ctx.author
        try:
            result = await rpgDb.get_player_absbonuses(self.bot.dbPool, str(player.id))
            if result is None:
                await ctx.send(f'Error fetching bonuses for player {player.display_name}')
                return
            embedMsg = Embed(color=0x00ff00)
            values = ''
            for bon in result:
                if search:
                    if search in bon[0].lower(): values += f'{bon[0]}: {bon[1]}\n'
                elif bon[1] != 0:values += f'{bon[0]}: {bon[1]}\n'
            embedMsg.add_field(name=f"{player.display_name} bonuses",value=values, inline=False)
            await ctx.send(embed=embedMsg)
        except Exception as e:
            print(e)
            await ctx.send('Error fetching player bonuses')
    
    @commands.hybrid_command(name='player', aliases=['pl'])
    async def show_abilities(self, ctx:Context, player: Optional[Member]):
        '''Shows information about the player from the event'''
        if not player:
            player = ctx.author
        #
        result = await rpgDb.get_player_info(self.bot.dbPool, str(player.id))
        if result is None:
            await ctx.send('Error fetching player info')
            return
        if result == []:
            await ctx.send('Player not found')
            return
        embedMsg = Embed(title=player.name.capitalize(), color=0x23dfeb)
        embedMsg.set_thumbnail(url=player.avatar)
        embedMsg.add_field(name='Chosen Dino',value=result['dino_type'], inline=True)
        embedMsg.add_field(name='\u200b', value='\u200b')
        embedMsg.add_field(name='Dino Name',value=result['dino_name'], inline=True)
        embedMsg.add_field(name='',value='**Dino Personality: **'+result['dino_personality'], inline=False)
        embedMsg.add_field(name='',value='**Dino Shiny Essence: **'+result['dino_shiny_essence'], inline=False)
        embedMsg.add_field(name='',value='**Dino Imprinting: **'+str(result['dino_imprinting'])+'%', inline=False)
        embedMsg.add_field(name='',value='**Dino Relationship: **'+str(result['dino_relationship']), inline=False)
        embedMsg.add_field(name='',value='**Base Companionship Level: **'+str(result['companionship_lvl']), inline=False)
        if not result['saddle_mastery']==0:
            embedMsg.add_field(name='',value='**Saddle Mastery Path: **'+str(result['saddle_mastery']), inline=False)
        if not result['dino_companionship']==0:
            embedMsg.add_field(name='',value='**Dino Companionship Path: **'+str(result['dino_companionship']), inline=False)
        if not result['capacity']==0:
            embedMsg.add_field(name='',value='**Capacity Path: **'+str(result['capacity']), inline=False)
        if not result['studious_mastery']==0:
            embedMsg.add_field(name='',value='**Studious Mastery Path: **'+str(result['studious_mastery']), inline=False)
        dinoClassifications = await rpgDb.get_player_classifications(self.bot.dbPool, str(player.id))
        if dinoClassifications is None:
            await ctx.send('Error fetching player classifications')
            return
        if len(dinoClassifications) > 1: 
            embedMsg.add_field(name='Dino Classifications: ',value='\n'.join(dinoClassifications), inline=True) 
            embedMsg.add_field(name='\u200b', value='\u200b')
        elif len(dinoClassifications) == 1:
            embedMsg.add_field(name='Dino Classifications: ',value=dinoClassifications[0], inline=True)
            embedMsg.add_field(name='\u200b', value='\u200b')
        dinoCapacities = await rpgDb.get_player_capacities(self.bot.dbPool, str(player.id))
        if dinoCapacities is None:
            await ctx.send('Error fetching player capacities')
            return
        if len(dinoCapacities) > 1: embedMsg.add_field(name='Dino Capacities: ',value='\n'.join(dinoCapacities), inline=True)
        elif len(dinoCapacities) == 1: embedMsg.add_field(name='Dino Capacities: ',value=dinoCapacities[0], inline=True)
        embedMsg.set_footer(text='dino is '+result['dino_status'])
        await ctx.send(embed=embedMsg)
        
    @commands.hybrid_command(name='players', aliases=['pls'])
    async def show_players(self,  ctx: Context, *, args: Optional[str] = None):
        '''Shows players that are participating in the event'''
        search = None
        if args:
            search = args.lower()
        result = await rpgDb.get_players(self.bot.dbPool, search)
        if result is None:
            await ctx.send('Error fetching players')
            return
        #pagination
        try:
            pageSource = PlayersPageSource(result, per_page=10)
            menu = menus.MenuPages(pageSource)
            await ctx.send('Players:', ephemeral=True)
            await menu.start(ctx)
        except Exception as e:
            print(e)
            
    @commands.hybrid_command(name='inventory', aliases=['inv'])
    async def get_inventory(self, ctx: Context):
        '''Shows the group inventory'''
        result = await rpgDb.get_inventory(self.bot.dbPool)
        if result is None:
            await ctx.send('Error fetching inventory')
            return
        embedMsg = self.formatInventory(result)
        await ctx.send(embed=embedMsg)
        
async def setup(bot):
    await bot.add_cog(RPG_Event(bot))