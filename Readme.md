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

#Current implemented systems:
##Notes:
At the moment, it consist only of 2 functions, when any is used, a pinned message is updated with all the notes saved (optional).
*add note
⋅⋅Adds a note
*del note
⋅⋅Removes a note

| Command                 | Slash/prefix | Roles |
| :---------------------- | :----------: | ----: |
| /addnote,?addnote,?n    |     both     |   any |
| /delnote, ?delnote, ?dn |     both     |   any |
