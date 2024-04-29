#python -m pip freeze > requirements.txt

TODO

4. Hatchery
5. Merchants
6. Logger

For hatchery:
const stageList = {
0 : 'Done',
1 : 'Baby',
2 : 'Juvenile',
3 : 'Adolecent',
4 : 'Training',
};
const rpgHatcherySchema = new Schema{
GuildID: String,
dinoName: String,
dinoProgress: Number,
dinoMaxProgress: Number,
dinoStage: String,
}

## Important Info

There are prefix and slash commands, and a command can be used with one, or both. For this bot, i made the prefix to be ?
So a command can be called like /command, or ?command.
Prefix commands are easier and quicker to use. But are tedious to configure when there are arguments required, like an update or addition to an inventory.
Slash commands in contrast, can be configured much easier, even with multiple requirements, also the arguments can be autocompleted from a list of choices.

# Implemented systems

### Basic event info:

There's a table where some special data is stored, general information for the bot, and from the event. Included the ids of messages that would be edited each time certain inventories are updated, as well as, the current group imprint bonus. And any new data that affects the entire group should be added here.

| Command       | Slash/prefix | Roles |
| :------------ | :----------: | ----: |
| /geteventdata |    slash     | admin |
| /seteventdata |    slash     | admin |

- geteventdata
  ⋅⋅ Displays a message with the discord server event related information. This is mostly for testing purposes.
  It shows:
  - server id
  - event-info channel id
  - info-msg id (this one is where the imprint bonus can be shown)
  - inventory msg id (this one is where the group inventory can be shown)
  - caravan msg id (deprecated atm)
  - caravan slots (deprecated)
  - notes msg id (this is where the notes will be shown)
  - imprint bonus (current group imprint bonus)
- seteventdata
  ⋅⋅ Updates the aforementioned information
  Example: /seteventdata imprint_bonus:140
  Required arguments: None
  Optional arguments: all of the above

###### TODO:

### Notes:

At the moment, it consist only of 2 functions, when any is used, a pinned message is updated with all the notes saved (optional).

| Command                 | Slash/prefix | Roles |
| :---------------------- | :----------: | ----: |
| /addnote,?addnote,?n    |     both     |   any |
| /delnote, ?delnote, ?dn |     both     |   any |

- add note
  ⋅⋅ Adds a note, I implemented the prefix use ?n, so its pretty easy and quick to add a note by just typing ?n this is a note
- del note
  ⋅⋅ Removes a note, it uses an id to delete a note, so it would be ?dn 2.

###### TODO: implement a command that retrieves and shows the list of currently added notes. Also add the possibility to add tags to each note, so they can be filtered on search.

### Inventory:

The inventory system, allows to manage the items found by the group during the event sessions.

| Command  | Slash/prefix | Roles |
| :------- | :----------: | ----: |
| /setitem |    slash     | admin |
| /delitem |    slash     | admin |

- setitem
  ⋅⋅ With this command, an item can be added or updated, for an item to be added only needs the name, so the command can be called using /setitem Sun berry
  For the same item to be updated, it needs to write the same name, plus any aditional data to be updated: /setitem "Sun berry" "Raw Plants"
  Required arguments: Item Name
  Optional arguments: Item class, item category, item quantity
- delitem
  ⋅⋅ Removes an item from the inventory, by calling its name
  Example: /delitem 'Sun berry'
  Required arguments: item name

###### TODO:Implement recipes
