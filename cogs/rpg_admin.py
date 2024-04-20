from re import search
from typing import Literal, Optional
from discord.ext import commands
from discord import Interaction, Member, app_commands
import queries.rpg.admin_queries as db
from queries.rpg.user_queries import get_ability_rolls

class RPG_Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.abilities = []
        
    async def cog_check(self, ctx) -> bool:
        if not(int(ctx.guild.id) == int(self.bot.allowedGuild) or int(ctx.guild.id) == int(self.bot.testingGuildId)):
            await ctx.send(f'Bot command only works on selected servers')
            return False
        if not ctx.permissions.manage_channels:
            await ctx.send(f'You do not have permission to use this command')
            return False
        return True
    
    async def ability(self)-> None:
        self.abilities = [ability[0] for ability in await get_ability_rolls(self.bot.dbPool)]
    
    async def cog_load(self):
        await self.ability()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('RPG config cog is ready!')
        
    
    @commands.command()
    async def testadmin(self, ctx, *args):
        '''This is a test command'''
        test:str = ' '.join(args)
        await ctx.send(f'test {test.capitalize()}')
    
    @app_commands.command(name='regdino')
    @app_commands.describe(type='The dino to add')
    async def register_dino(self, interaction: Interaction, type: str):
        """Registers a new dino type to be available for the event"""
        try:
            await db.register_dino_type(self.bot.dbPool, type.capitalize())
            await interaction.response.send_message(f'Dino {type} registered')
        except Exception as e:
            await interaction.response.send_message(f'Error: Failed to register {type} dino')
                
    @commands.command(name='deldino')
    async def delete_dino(self, ctx, *args):
        '''TODO Delete a dino type from the list for the event'''
        dino:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @app_commands.command(name='setclassification')
    @app_commands.describe(clas='The classification to add or edit')
    @app_commands.rename(clas='classification')
    @app_commands.describe(description='The classification description to add or update')
    @app_commands.describe(bonus='The classification bonus to add or update')
    async def set_classification(self, interaction: Interaction, clas: str, description: Optional[str], bonus: Optional[str]):
        """Registers or edits a dino classification"""
        try:
            await db.register_classification(self.bot.dbPool, clas.capitalize(), description, bonus)
            await interaction.response.send_message(f'Classification {clas} registered or updated')
        except Exception as e:
            await interaction.response.send_message(f'Error: Failed to set {clas} classification')
        
    @commands.command(name='delclass')
    async def delete_class(self, ctx, *args):
        '''TODO Delete class'''
        clas:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @app_commands.command(name='setcapacity')
    @app_commands.describe(capacity='The capacity to add or edit')
    @app_commands.describe(description='The capacity description to add or update')
    async def set_capacity(self, interaction: Interaction, capacity: str, description: Optional[str]):
        """Registers or edits a dino capacity"""
        try:
            await db.register_dino_capacity(self.bot.dbPool, capacity.capitalize(), description)
            await interaction.response.send_message(f'Capacity {capacity} registered or updated')
        except Exception as e:
            await interaction.response.send_message(f'Error: Failed to set {capacity} capacity')
    
    @commands.command(name='delcap')
    async def delete_capacity(self, ctx, *args):
        '''TODO Delete capacity'''
        cap:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @app_commands.command(name='setessence')
    @app_commands.describe(ess='The Essence to add or edit')
    @app_commands.rename(ess='essence')
    @app_commands.describe(description='The Essence description to add or update')
    @app_commands.describe(mastery='The Essence mastery bonus to add or update')
    async def set_essence(self, interaction: Interaction, ess: str, description: Optional[str], mastery: Optional[str]):
        """Registers or edits a dino Shiny Essence"""
        try:
            await db.register_essence(self.bot.dbPool, ess.capitalize(), description, mastery)
            await interaction.response.send_message(f'Essence {ess} registered or updated')
        except Exception as e:
            await interaction.response.send_message(f'Error: Failed to set {ess} shiny essence')
        
    @commands.command(name='deless')
    async def delete_essence(self, ctx, *args):
        '''TODO Delete shiny essence'''
        ess:str = ' '.join(args)
        await ctx.send(f'to be implemented...')
        
    @app_commands.command(name='setability')
    @app_commands.describe(ability='The ability roll to add or edit')
    @app_commands.describe(description='The ability roll description to add or update')
    async def set_ability(self, interaction: Interaction, ability: str, description: Optional[str]):
        """Registers or edits ability rolls for the event"""
        try:
            await db.register_ability(self.bot.dbPool, ability.capitalize(), description)
            await interaction.response.send_message(f'Ability {ability} registered or updated')
        except Exception as e:
            await interaction.response.send_message(f'Error: Failed to set {ability} ability')
        
    @commands.command(name='delability')
    async def Delete_abilityroll(self, ctx, *args):
        '''TODO Delete ability roll'''
        await ctx.send(f'to be implemented...')
    
    @app_commands.command(name='setbonus')
    @app_commands.describe(player='The player to add the bonus to')
    @app_commands.describe(ability='The ability to update')
    @app_commands.describe(bonus='The bonus to add to an ability roll, can be absoulte or with operators + or -')
    async def set_ability_bonus(self, interaction: Interaction,player:Member, ability: str, bonus: str):
        '''Adds a bonus to a specified player ability (player tek +1)'''
        ogBonus = bonus
        op = None
        if(bonus[0] == '+' or bonus[0] == '-'):
            op = bonus[0]
            try:bonus = int(bonus[1:])
            except:
                await interaction.response.send_message(f'Invalid bonus value')
                return
        else:
            try:bonus = int(bonus)
            except:
                await interaction.response.send_message(f'Invalid bonus value')
                return
        try:
            await db.set_player_bonus_roll(self.bot.dbPool, str(player.id), ability, bonus, op)
            await interaction.response.send_message(f'Set {ogBonus} to {ability} ability for {player.display_name}')
        except Exception as e:
            print(e)
            await interaction.response.send_message(f'Error: Failed to set {ability} bonus')
    
    @set_ability_bonus.autocomplete('ability')
    async def autocomplete_ability(self,interaction: Interaction, current: str):
        # Do stuff with the "current" parameter, e.g. querying it search results...
        search_results=[]
        for ability in self.abilities:
            if search(current.lower(), ability.lower()):
                search_results.append(app_commands.Choice(name=ability,value=ability))
        # Then return a list of app_commands.Choice
        return search_results
    
    @app_commands.command(name='addplayer')
    @app_commands.describe(player='The player register for the event')
    @app_commands.describe(dino_type='The chosen dino')
    @app_commands.describe(dino_name='The chosen dino name')
    async def add_player(self, interaction: Interaction,player:Member, dino_type: str, dino_name: str):
        '''Register event player'''
        try: 
            await db.register_player(self.bot.dbPool, str(player.id), player.display_name, dino_type, dino_name)
            await interaction.response.send_message(f'accepted')
        except Exception as e:
            print(e)
            await interaction.response.send_message(f'Error: Failed to add {player.display_name}')
    #todo dino_type autocomplete
    
    @app_commands.command(name='setplayer')
    @app_commands.describe(player='The player set the data for')
    async def set_player(self, interaction: Interaction,player:Member, dino_type: Optional[str], 
                         dino_name: Optional[str], dino_status: Optional[str], dino_personality: Optional[str],
                         dino_essence: Optional[str], dino_imprinting: Optional[int], dino_relationship: Optional[int],
                         companionship_lvl:Optional[int], saddle_mastery: Optional[int], dino_companionship: Optional[int],
                         capacity: Optional[int], studious_mastery: Optional[int]):
        '''Updates informations for the selected player'''
        try: 
            await db.set_player_data(self.bot.dbPool, str(player.id), dino_type, dino_name, dino_status, dino_personality,
                                     dino_essence, dino_imprinting, dino_relationship, companionship_lvl, saddle_mastery,
                                     dino_companionship, capacity, studious_mastery)
            await interaction.response.send_message(f'accepted')
        except Exception as e:
            print(e)
            await interaction.response.send_message(f'Error: Failed to update player, does {player.display_name} exists?')
    
    @commands.command(name='delplayer')
    async def register_player(self, ctx, *args):
        '''TODO Delete event player'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='addplayerclass')
    async def add_player_classification(self, ctx, *args):
        '''TODO Add player dino classification'''
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='delplayerclass')
    async def delete_player_classification(self, ctx, *args):
        '''TODO Delete player dino classification'''
        await ctx.send(f'to be implemented...')
    
    @commands.command(name='addplayercap')
    async def add_player_capacity(self, ctx, *args):
        '''TODO Add player dino capacity'''
        await ctx.send(f'to be implemented...')
        
    @commands.command(name='delplayercap')
    async def delete_player_capacity(self, ctx, *args):
        '''TODO Delete player dino capacity'''
        await ctx.send(f'to be implemented...')
    
    #todo setitem
    
    @app_commands.command(name='test')
    #@app_commands.choices(ability=
    async def add_item(self, interaction: Interaction, player:Member, ability: str) -> None:
        '''Test slash command'''
        await interaction.response.send_message('testing')
    
    
async def setup(bot):
    await bot.add_cog(RPG_Admin(bot))