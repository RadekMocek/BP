import net.dv8tion.jda.api...
// ...
public void onSlashCommandInteraction(SlashCommandInteractionEvent event) {
    if (event.getName().equals("pow")) {
        int num = event.getOption("num").getAsInt();
        int exp = event.getOption("exp").getAsInt();
        event.reply("" + Math.pow(num,exp)).addActionRow(Button.link("https://example.com", "Example")).queue();
    }
}