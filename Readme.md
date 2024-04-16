#python -m pip freeze > requirements.txt

todo
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

---

const rpgInfoSchemna = new Schema({
GuildID: String,
infoChannelID: String,
logsChannelID: String,
merchantsChannelID: String,
hatcheryChannelID: String,
}

---

const rpgInventorySchemna = new Schema({
GuildID: String,
Items: Array,
}

---

data: new SlashCommandBuilder()
.setName('rpg-setup')
.setDescription('Set the rpg channels')
.addChannelOption(option => option
.setName('rpg-info-channel')
.setDescription('The channel to post the main information about the rpg event')
.setRequired(true)
.addChannelTypes(ChannelType.GuildText))
.addChannelOption(option => option
.setName('logs-channel')
.setDescription('The channel to post rpg related bot log messages')
.setRequired(true)
.addChannelTypes(ChannelType.GuildText))
.addChannelOption(option => option
.setName('merchants-channel')
.setDescription('The channel to post and check the merchants information (will use the info if empty)')
.setRequired(false)
.addChannelTypes(ChannelType.GuildText))
.addChannelOption(option => option
.setName('hatchery-channel')
.setDescription('The channel to post and check the hatchery information (will use the info if empty)')
.setRequired(false)
.addChannelTypes(ChannelType.GuildText))
.setDefaultMemberPermissions(PermissionFlagsBits.ManageChannels),

---

data: new SlashCommandBuilder()
.setName('rpg-info')
.setDescription('Get the rpg related bot data'),
userPermissions: [PermissionFlagsBits.ManageChannels],
botPermissions: [],
run: async (client, interaction) => {
const { guild } = interaction;
const data = await rpgInfoSchema.findOne({ GuildID: guild.id });
if (!data) {
return interaction.reply({
content: '❌ The RPG Setup hasnt been done yet',
ephemeral: true,
});
}
else {
const dataEmbed = new EmbedBuilder()
.setTitle('⭐ RPG Information')
.setDescription(`
					**Info Channel: **${guild.channels.cache.get(data.infoChannelID)}
					\n**Logs Channel: **${guild.channels.cache.get(data.logsChannelID)}
					\n**Merchants Channel: **${guild.channels.cache.get(data.merchantsChannelID)}
					\n**Hatchery Channel: **${guild.channels.cache.get(data.hatcheryChannelID)}`);
return await interaction.reply({
embeds: [dataEmbed],
ephemeral: true,
});

---

rpgInventory
