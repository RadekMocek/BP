const {
    ActionRowBuilder, ButtonBuilder, ButtonStyle, SlashCommandBuilder
} = require("discord.js");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("pow")
        .setDescription("Umocní číslo 'num' na 'exp'.")
        .addIntegerOption(op => op.setName("num").setRequired(true))
        .addIntegerOption(op => op.setName("exp").setRequired(true)),
    async execute(interaction) {
        const num = interaction.options.getInteger("num");
        const exp = interaction.options.getInteger("exp");
        const button = new ButtonBuilder()
            .setLabel("Example")
            .setURL("https://example.com")
            .setStyle(ButtonStyle.Link);
        const row = new ActionRowBuilder().addComponents(button);
        await interaction.reply({
            content: "" + num ** exp, components: [row]
        });
    },
};