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

| Command       | Slash/prefix | Roles |
| :------------ | :----------: | ----: |
| /addnote,?n   |     both     |   any |
| /delnote, ?dn |     both     |   any |

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

### Player:

Player information, this is where each player can be registered, updated, or deleted.

| Command         | Slash/prefix | Roles |
| :-------------- | :----------: | ----: |
| /addplayer      |    slash     | admin |
| /setplayer      |    slash     | admin |
| /delplayer      |    slash     | admin |
| /addplayerclass |    slash     | admin |
| /delplayerclass |    slash     | admin |
| /addplayercap   |    slash     | admin |
| /delplayercap   |    slash     | admin |
| /setbonus       |    slash     | admin |
| /player, ?pl    |     both     |   any |
| /players, ?pls  |     both     |   any |
| /bonus, ?b      |     both     |   any |

- addplayer
  ⋅⋅This one registers a player as a participant for the event. A player must be registered before updating any information from him/her.
  ⋅⋅ Example: /addplayer Drykolf 'Phoenix' 'Yela'
  ⋅⋅ Required arguments: Player, Chosen dino (choices), Dino name
  ⋅⋅ Optional arguments: None
- setplayer
  ⋅⋅ Updates a player information.
  ⋅⋅ Example: /setplayer Drykolf
  ⋅⋅ Required arguments: Player
  ⋅⋅ Optional arguments: dino_type (choices), dino_name, dino_status (alive?), dino_personality(Unknown by default), dino_essence (shiny essence, choices), dino_imprinting, dino_relationship(happy?, choices?), companionship_lvl, saddle_mastery, dino_companionship, capacity_lvl, studious_mastery
- delplayer
  ⋅⋅ Removes the player information from the bot tables.
  ⋅⋅ Example: /delplayer Drykolf
  ⋅⋅ Required arguments: Player
- player
  ⋅⋅ This command displays a card with the information regarding the player. Can be own information, or another player's
  ⋅⋅ Example: ?pl
  ⋅⋅ Optional arguments: Player
- players
  ⋅⋅ Shows a list of the players registered for the event
  Example: ?players
- bonus
  ⋅⋅ Shows the bonus that a player has for any ability roll
  ⋅⋅ Example: ?b tek -> would show any bonus tek related, if no arguments, will show any bonus that has any points on
  ⋅⋅ Optional arguments: any word works as a search
- addplayerclass
  ⋅⋅ Adds a classification to the player
  ⋅⋅ Example: /addplayerclass Drykolf Bird
  ⋅⋅ Required arguments: Player, Classification (choices)
- delplayerclass
  ⋅⋅ Removes a classification from the player
  ⋅⋅ Example: /delplayerclass Drykolf Bird
  ⋅⋅ Required arguments: Player, Classification (choices)
- addplayercap
  ⋅⋅ Adds a capacity to the player
  ⋅⋅ Example: /addplayercap Drykolf Execute
  ⋅⋅ Required arguments: Player, Capacity (choices)
- addplayercap
  ⋅⋅ Adds a capacity to the player
  ⋅⋅ Example: /addplayercap Drykolf Execute
  ⋅⋅ Required arguments: Player, Capacity (choices)
- delplayercap
  ⋅⋅ Removes a capacity from the player
  ⋅⋅ Example: /delplayercap Drykolf Execute
  ⋅⋅ Required arguments: Player, Capacity (choices)
- setbonus
  ⋅⋅ Updates bonuses from the player, the bonus can be a direct value (2), or an addition/subtraction over the old bonus (+3)
  ⋅⋅ Example: /setbonus Drykolf Hunting +2
  ⋅⋅ Required arguments: Player, ability (choices), bonus

###### TODO:

# TODO

## Merchants

## Hatchery?

Dino stages
0 : 'Done'
1 : 'Baby'
2 : 'Juvenile'
3 : 'Adolecent'
4 : 'Training'

## Logger (to identify errors)

#python -m pip freeze > requirements.txt
