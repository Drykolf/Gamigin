from re import search
from typing import Optional
from discord.ext import commands
from discord import Interaction, Member, app_commands
import queries.rpg.admin_queries as db
from queries.rpg.user_queries import get_ability_rolls, get_player_info

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
        #Load abilities for autocomplete
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
        if await db.register_dino_type(self.bot.dbPool, type.capitalize()):
            await interaction.response.send_message(f'Dino {type} registered')
        else:
            await interaction.response.send_message(f'Error: Failed to register {type} dino')
    
    #TODO autocomplete
    @app_commands.command(name='deldino')
    @app_commands.describe(type='The dino to delete')
    async def delete_dino(self, interaction: Interaction, type: str):
        """Deletes a dino type from the selection"""
        result = await db.delete_dino_type(self.bot.dbPool, type.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {type} dino not found'
            else: msg = f'Dino {type} deleted'
        else: msg = f'Error: Failed to delete {type} dino'
        await interaction.response.send_message(msg)
    
    #TODO autocomplete
    @app_commands.command(name='setcapacity')
    @app_commands.describe(capacity='The capacity to add or edit')
    @app_commands.describe(description='The capacity description to add or update')
    async def set_capacity(self, interaction: Interaction, capacity: str, description: Optional[str]):
        """Registers or edits a dino capacity"""
        result = await db.set_dino_capacity(self.bot.dbPool, capacity.capitalize(), description)
        msg = ''
        if result: msg = f'Capacity {capacity} registered or updated'
        else: msg = f'Error: Failed to set {capacity} capacity'
        await interaction.response.send_message(msg)
        
    #TODO autocomplete
    @app_commands.command(name='delcapacity')
    @app_commands.describe(capacity='The capacity to delete')
    async def delete_capacity(self, interaction: Interaction, capacity: str):
        '''Deletes a capacity'''
        result = await db.delete_dino_capacity(self.bot.dbPool, capacity.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {capacity} not found'
            else: msg = f'{capacity} deleted'
        else: msg = f'Error: Failed to delete {capacity}'
        await interaction.response.send_message(msg)
        
    #TODO autocomplete
    @app_commands.command(name='setclassification')
    @app_commands.describe(clas='The classification to add or edit')
    @app_commands.rename(clas='classification')
    @app_commands.describe(description='The classification description to add or update')
    @app_commands.describe(bonus='The classification bonus to add or update')
    async def set_classification(self, interaction: Interaction, clas: str, description: Optional[str], bonus: Optional[str]):
        """Registers or edits a dino classification"""
        if await db.set_classification(self.bot.dbPool, clas.capitalize(), description, bonus):
            await interaction.response.send_message(f'Classification {clas} registered or updated')
        else:
            await interaction.response.send_message(f'Error: Failed to set {clas} classification')
    
    #TODO autocomplete
    @app_commands.command(name='delclassification')
    @app_commands.rename(clas='classification')
    @app_commands.describe(clas='The classification to delete')
    async def delete_class(self, interaction: Interaction, clas: str):
        '''Deletes a classification'''
        result = await db.delete_classification(self.bot.dbPool, clas.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {clas} not found'
            else: msg = f'{clas} deleted'
        else: msg = f'Error: Failed to delete {clas}'
        await interaction.response.send_message(msg)
    
    #TODO autocomplete
    @app_commands.command(name='setability')
    @app_commands.describe(ability='The ability roll to add or edit')
    @app_commands.describe(description='The ability roll description to add or update')
    async def set_ability(self, interaction: Interaction, ability: str, description: Optional[str]):
        """Registers or edits ability rolls for the event"""
        if await db.set_ability(self.bot.dbPool, ability.capitalize(), description):
            await self.ability()
            await interaction.response.send_message(f'Ability {ability} registered or updated')
        else:
            await interaction.response.send_message(f'Error: Failed to set {ability} ability')
    
    #TODO autocomplete
    @app_commands.command(name='delability')
    @app_commands.describe(ability='The ability roll to remove')
    async def Delete_abilityroll(self, interaction: Interaction, ability: str):
        '''Delete ability roll'''
        result = await db.delete_ability(self.bot.dbPool, ability.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {ability} not found'
            else: 
                await self.ability()
                msg = f'{ability} deleted'
        else: msg = f'Error: Failed to delete {ability}'
        await interaction.response.send_message(msg)
        
    #TODO autocomplete
    @app_commands.command(name='setessence')
    @app_commands.describe(ess='The Essence to add or edit')
    @app_commands.rename(ess='essence')
    @app_commands.describe(description='The Essence description to add or update')
    @app_commands.describe(mastery='The Essence mastery bonus to add or update')
    async def set_essence(self, interaction: Interaction, ess: str, description: Optional[str], mastery: Optional[str]):
        """Registers or edits a dino Shiny Essence"""
        if await db.set_essence(self.bot.dbPool, ess.capitalize(), description, mastery):
            await interaction.response.send_message(f'Essence {ess} registered or updated')
        else:
            await interaction.response.send_message(f'Error: Failed to set {ess} shiny essence')
        
    #TODO autocomplete
    @app_commands.command(name='delessence')
    @app_commands.describe(ess='The Essence to remove')
    @app_commands.rename(ess='essence')
    async def delete_essence(self, interaction: Interaction, ess: str):
        '''Delete shiny essence'''
        result = await db.delete_essence(self.bot.dbPool, ess.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {ess} not found'
            else: msg = f'{ess} deleted'
        else: msg = f'Error: Failed to delete {ess}'
        await interaction.response.send_message(msg)
    
    #todo dino_type autocomplete
    @app_commands.command(name='addplayer')
    @app_commands.describe(player='The player register for the event')
    @app_commands.describe(dino_type='The chosen dino')
    @app_commands.describe(dino_name='The chosen dino name')
    async def add_player(self, interaction: Interaction,player:Member, dino_type: str, dino_name: str):
        '''Register event player'''
        if await db.register_player(self.bot.dbPool, str(player.id), player.display_name.capitalize(), dino_type.capitalize(), dino_name.capitalize()):
            await interaction.response.send_message(f'accepted')
        else:
            await interaction.response.send_message(f'Error: Failed to add {player.display_name}')
    
    #TODO autocomplete
    @app_commands.command(name='setplayer')
    @app_commands.describe(player='The player set the data for')
    async def set_player(self, interaction: Interaction,player:Member, dino_type: Optional[str], 
                         dino_name: Optional[str], dino_status: Optional[str], dino_personality: Optional[str],
                         dino_essence: Optional[str], dino_imprinting: Optional[int], dino_relationship: Optional[int],
                         companionship_lvl:Optional[int], saddle_mastery: Optional[int], dino_companionship: Optional[int],
                         capacity: Optional[int], studious_mastery: Optional[int]):
        '''Updates informations for the selected player (needs to be already registered)'''
        result = await db.update_player_data(self.bot.dbPool, str(player.id), dino_type.capitalize(), dino_name.capitalize(), dino_status.capitalize(), dino_personality.capitalize(),
                                     dino_essence.capitalize(), dino_imprinting, dino_relationship, companionship_lvl, saddle_mastery,
                                     dino_companionship, capacity, studious_mastery)
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {player.display_name} not found'
            else: msg = f'{player.display_name} updated'
        else: msg = f'Error: Failed to update {player.display_name}'
        await interaction.response.send_message(msg)
    
    @app_commands.command(name='delplayer')
    @app_commands.describe(player='The player to remove')
    async def delete_player(self, interaction: Interaction,player:Member):
        '''Delete event player'''
        result = await db.delete_player(self.bot.dbPool, str(player.id))
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {player.display_name} not found'
            else: msg = f'{player.display_name} deleted'
        else: msg = f'Error: Failed to delete {player.display_name}'
        await interaction.response.send_message(msg)
    
    @app_commands.command(name='addplayerclass')
    @app_commands.describe(player='The player set the data for')
    @app_commands.describe(clas='The classification to add')
    @app_commands.rename(clas='classification')
    async def add_player_classification(self, interaction: Interaction,player:Member, clas: str):
        '''Add a player dino classification'''
        playerInfo = await get_player_info(self.bot.dbPool, str(player.id))
        if playerInfo is None:
            await interaction.response.send_message('Error fetching player info')
            return
        if playerInfo == []:
            await interaction.response.send_message('Player not found')
            return
        if await db.add_class_player(self.bot.dbPool, str(player.id), clas.capitalize()):
            await interaction.response.send_message(f'accepted')
        else:
            await interaction.response.send_message(f'Error: Failed to add {clas} classification to {player.display_name}')
    
    @app_commands.command(name='delplayerclass')
    @app_commands.describe(player='The player to remove the classification from')
    @app_commands.describe(clas='The classification to remove')
    @app_commands.rename(clas='classification')
    async def delete_player_classification(self, interaction: Interaction,player:Member, clas: str):
        '''Delete player dino classification'''
        result = await db.remove_class_player(self.bot.dbPool, str(player.id), clas.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {clas} not found'
            else: msg = f'{clas} deleted'
        else: msg = f'Error: Failed to delete {clas}'
        await interaction.response.send_message(msg)
        
    @app_commands.command(name='addplayercap')
    @app_commands.describe(player='The player to add the capacity to')
    @app_commands.describe(capacity='The capacity to add')
    async def add_player_capacity(self, interaction: Interaction,player:Member, capacity: str):
        '''Add a player dino capacity'''
        playerInfo = await get_player_info(self.bot.dbPool, str(player.id))
        if playerInfo is None:
            await interaction.response.send_message('Error fetching player info')
            return
        if playerInfo == []:
            await interaction.response.send_message('Player not found')
            return
        if await db.add_cap_player(self.bot.dbPool, str(player.id), capacity.capitalize()):
            await interaction.response.send_message(f'accepted')
        else:
            await interaction.response.send_message(f'Error: Failed to add {capacity} capacity to {player.display_name}')
    
    @app_commands.command(name='delplayercap')
    @app_commands.describe(player='The player to remove the capacity from')
    @app_commands.describe(capacity='The capacity to remove')
    async def delete_player_capacity(self, interaction: Interaction,player:Member, capacity: str):
        '''Delete player dino capacity'''
        result = await db.remove_cap_player(self.bot.dbPool, str(player.id), capacity.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {capacity} not found'
            else: msg = f'{capacity} deleted'
        else: msg = f'Error: Failed to delete {capacity}'
        await interaction.response.send_message(msg)
    
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
        if await db.set_player_bonus_roll(self.bot.dbPool, str(player.id), ability.capitalize(), bonus, op):
            await interaction.response.send_message(f'Set {ogBonus} to {ability} ability roll for {player.display_name}')
        else:
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
    
    
    
    #todo setitem
    
    
async def setup(bot):
    await bot.add_cog(RPG_Admin(bot))