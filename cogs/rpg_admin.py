from re import search
from tkinter import E
from typing import Optional
from discord.ext import commands
from discord import Embed, Interaction, Member, NotFound, app_commands, TextChannel
import cogs.queries.db_admin as db
from cogs.queries.db_user import get_ability_rolls, get_player_info

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
    
    async def update_items_msg(self,interaction: Interaction) -> None:
        if (str(interaction.guild_id) in self.bot.guildData):
            data = self.bot.guildData[str(str(interaction.guild_id))]
            if (data['event_chnel_id']!=None and data['event_chnel_id'] != '0'):
                channel = interaction.guild.get_channel(int(data['event_chnel_id']))
                match data['inv_msg_id']:
                    case None: return
                    case '0': return
                    case '1': 
                        msg = await channel.send(embed=Embed(title='===The Group Event Inventory===', 
                                                             description='Everyone has access to this inventory during the event regardless of location'))
                        await db.set_guild_data(self.bot.dbPool, str(interaction.guild_id), inv_msg_id=str(msg.id))
                        data['inv_msg_id'] = str(msg.id)
                        await self.bot.load_guilds()
                try:
                    itemsMsg = channel.get_partial_message(int(data['inv_msg_id']))
                    if (items := await db.get_items(self.bot.dbPool)) is not None:
                        invContent = self.formatInventory(items)
                        await itemsMsg.edit(embed=invContent)
                except NotFound as e:
                    await db.set_guild_data(self.bot.dbPool, str(interaction.guild_id), inv_msg_id='0')
                    data['inv_msg_id'] = '0'
                    await self.bot.load_guilds()
                except Exception as e:
                    print(f'update item msg error: {e}')
                    #log error
    
    async def update_caravan_msg(self,interaction: Interaction) -> None:
        if (str(interaction.guild_id) in self.bot.guildData):
            data = self.bot.guildData[str(str(interaction.guild_id))]
            if (data['event_chnel_id']!=None and data['event_chnel_id'] != '0'):
                channel = interaction.guild.get_channel(int(data['event_chnel_id']))
                match data['caravan_msg_id']:
                    case None: return
                    case '0': return
                    case '1': 
                        msg = await channel.send(embed=Embed(title='Caravan Information', description='Campaign related caravan information:'))
                        await db.set_guild_data(self.bot.dbPool, str(interaction.guild_id), caravan_msg_id=str(msg.id))
                        data['caravan_msg_id'] = str(msg.id)
                        await self.bot.load_guilds()
                sDinos = 0
                mDinos = 0
                lDinos = 0
                result = None
                try:
                    result = await db.get_caravan(self.bot.dbPool)
                except Exception as e:
                    print(f'fetch caravan msg error: {e}')
                    #log error
                if result:
                    for dino in result:
                        if dino[2] == 1: sDinos += 1
                        if dino[2] == 2: mDinos += 1
                        if dino[2] == 3: lDinos += 1
                msg = Embed()
                content = f'Little Dinos: {sDinos}/{data["caravan_sslots"]} \n Medium Dinos: {mDinos}/{data["caravan_mslots"]} \n Large Dinos: {lDinos}/{data["caravan_lslots"]}'
                msg.add_field(name='Caravan Capacity', value=content)
                try:
                    caravanMsg = channel.get_partial_message(int(data['caravan_msg_id']))
                    await caravanMsg.edit(embed=msg)
                except NotFound as e:
                    await db.set_guild_data(self.bot.dbPool, str(interaction.guild_id), caravan_msg_id='0')
                    data['caravan_msg_id'] = '0'
                    await self.bot.load_guilds()
                except Exception as e:
                    print(f'update caravan msg error: {e}')
                    #log error
                    
    async def update_info_msg(self,interaction: Interaction) -> None:
        if (str(interaction.guild_id) in self.bot.guildData):
            data = self.bot.guildData[str(str(interaction.guild_id))]
            if (data['event_chnel_id']!=None and data['event_chnel_id'] != '0'):
                channel = interaction.guild.get_channel(int(data['event_chnel_id']))
                match data['info_msg_id']:
                    case None: return
                    case '0': return
                    case '1': 
                        msg = await channel.send(embed=Embed(title='Event Information', description='Campaign related basic information:'))
                        await db.set_guild_data(self.bot.dbPool, str(interaction.guild_id), info_msg_id=str(msg.id))
                        data['info_msg_id'] = str(msg.id)
                        await self.bot.load_guilds()
                try:
                    infoMsg = channel.get_partial_message(int(data['info_msg_id']))
                    msg = Embed(title='Event Information', description='Campaign related basic information:')
                    msg.add_field(name='', value=f'**Imprinting Bonus:** {data["imprint_bonus"]}%')
                    await infoMsg.edit(embed=msg)
                except NotFound as e:
                    await db.set_guild_data(self.bot.dbPool, str(interaction.guild_id), info_msg_id='0')
                    data['info_msg_id'] = '0'
                    await self.bot.load_guilds()
                except Exception as e:
                    print(f'update info msg error: {e}')
                    #log error
                    
    @commands.command()
    async def testadmin(self, ctx, *args):
        '''This is a test command'''
        test:str = ' '.join(args)
        print(self.bot.guildData)
        await ctx.send(f'test {test.capitalize()}')
    
    @app_commands.command(name='geteventdata')
    async def get_event_data(self, interaction: Interaction):
        '''Get the bot event data'''
        msg = 'Not yet set'
        if (str(interaction.guild_id) in self.bot.guildData):
            data = self.bot.guildData[str(interaction.guild_id)]
            msg = (f"Guild ID: {data['guild_id']} \n Event Channel ID: {data['event_chnel_id']} \n Info Message ID: {data['info_msg_id']} \n Inventory Message ID: {data['inv_msg_id']} \n" +
                f"Caravan Message ID: {data['caravan_msg_id']} \n Notes Message ID: {data['notes_msg_id']} \n Caravan Small Slots: {data['caravan_sslots']} \n" +
                f"Caravan Medium Slots: {data['caravan_mslots']} \n Caravan Large Slots: {data['caravan_lslots']} \n Imprint Bonus: {data['imprint_bonus']}%")
        await interaction.response.send_message(msg)
    
    #TODO descriptions
    @app_commands.command(name='seteventdata')
    async def set_guild(self, interaction:Interaction, event_channel:Optional[TextChannel], info_msg:Optional[str], 
                        inv_msg:Optional[str], caravan_msg:Optional[str], notes_msg:Optional[str], caravan_sslots:Optional[int], 
                        caravan_mslots:Optional[int], caravan_lslots:Optional[int], imprint_bonus:Optional[int]):
        '''Set the event data'''
        if event_channel: event_channel = str(event_channel.id)
        await interaction.response.defer()
        try:
            if not(str(interaction.guild_id) in self.bot.guildData):
                if not await db.register_guild(self.bot.dbPool, str(interaction.guild_id)):
                    await interaction.followup.send('Error: Failed to register server info')
                    return
            result = await db.set_guild_data(self.bot.dbPool, str(interaction.guild_id), event_channel, info_msg, inv_msg, caravan_msg, 
                                            notes_msg, caravan_sslots, caravan_mslots, caravan_lslots, imprint_bonus)
            msg = ''
            if(result):
                if(result[-1] == '0'): msg = f'Nothing updated'
                else: 
                    msg = f'Event info updated'
                    await self.bot.load_guilds()
                    if(info_msg is not None or imprint_bonus is not None): await self.update_info_msg(interaction)
                    if(caravan_msg is not None or caravan_sslots is not None or caravan_mslots is not None or caravan_lslots is not None): await self.update_caravan_msg(interaction)
            else: msg = f'Error: Failed to update event info'
            await interaction.followup.send(msg)
        except Exception as e:
            print(e)
        
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
        if dino_type: dino_type = dino_type.capitalize()
        if dino_name: dino_name = dino_name.capitalize()
        if dino_status: dino_status = dino_status.capitalize()
        if dino_personality: dino_personality = dino_personality.capitalize()
        if dino_essence: dino_essence = dino_essence.capitalize()
        result = await db.update_player_data(self.bot.dbPool, str(player.id), dino_type, dino_name, dino_status, dino_personality,
                                    dino_essence, dino_imprinting, dino_relationship, companionship_lvl, saddle_mastery,
                                    dino_companionship, capacity, studious_mastery)
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {player.display_name} not updated/not found'
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
    
    #TODO autocomplete
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
    
    #TODO autocomplete
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
    
    #TODO autocomplete
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
    
    #TODO autocomplete
    @app_commands.command(name='setitem')
    @app_commands.describe(item='The item to add or update')
    async def set_item(self, interaction: Interaction, item: str, item_class:Optional[str], item_cat:Optional[str], item_quantity:Optional[str]):
        '''Registers or edits an item for the event'''
        await interaction.response.defer()
        op = None
        if item_quantity:
            if(item_quantity[0] == '+' or item_quantity[0] == '-'):
                op = item_quantity[0]
                item_quantity=item_quantity[1:]
            try:item_quantity = int(item_quantity)
            except:
                await interaction.response.send_message(f'Invalid quantity value')
                return
        if item: item = item.capitalize()
        if item_class: item_class = item_class.capitalize()
        if item_cat: item_cat = item_cat.capitalize()
        try: 
            result = await db.set_item(self.bot.dbPool, item, item_class, item_cat, item_quantity, op)
            msg = ''
            if result: 
                if(result[-1] == '0'): 
                    msg = f'Item {item} added if didnt existed, no changes made'
                    await self.update_items_msg(interaction)
                else: 
                    msg = f'Item {item} updated'
                    await self.update_items_msg(interaction)
            else: msg = f'Error: Failed to set {item} item'
            await interaction.followup.send(msg)
        except Exception as e:
            print(e)
        
    #TODO autocomplete?
    @app_commands.command(name='delitem')
    @app_commands.describe(item='The item to delete')
    async def delete_item(self, interaction: Interaction, item: str):
        '''Delete item'''
        await interaction.response.defer()
        result = await db.delete_item(self.bot.dbPool, item.capitalize())
        msg = ''
        if(result):
            if(result[-1] == '0'): msg = f'Error: {item} not found'
            else: 
                await self.update_items_msg(interaction)
                msg = f'{item} deleted'
        else: msg = f'Error: Failed to delete {item}'
        await interaction.followup.send(msg)
        
    #TODO autocomplete dinoTpe
    @app_commands.command(name='addcaravan')
    @app_commands.describe(dino_type='The dino to add to the caravan')
    @app_commands.describe(dino_name='The dino name')
    @app_commands.describe(dino_size='The dino size')
    @app_commands.choices(dino_size=[
        app_commands.Choice(name='Small', value=1), 
        app_commands.Choice(name='Medium', value=2), 
        app_commands.Choice(name='Large', value=3),
        app_commands.Choice(name='Platform', value=0)])
    async def add_caravan(self, interaction: Interaction, dino_type: str, dino_size: int, dino_name: Optional[str]=None):
        '''Add a dino to the caravan'''
        if(dino_name): dino_name = dino_name.capitalize()
        if await db.add_caravan_dino(self.bot.dbPool, dino_type.capitalize(), dino_name, dino_size):
            await interaction.response.send_message(f'accepted')
            await self.update_caravan_msg(interaction)
        else:
            await interaction.response.send_message(f'Error: Failed to add {dino_type} to the caravan')
    
async def setup(bot):
    await bot.add_cog(RPG_Admin(bot))