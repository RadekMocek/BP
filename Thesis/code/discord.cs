using Discord;
using Discord.WebSocket;

private async Task SlashCommandHandler(SocketSlashCommand command) {
    if (command.Data.Name == "pow") {
        var num = (Int64)command.Data.Options.ElementAt(0).Value;
        var exp = (Int64)command.Data.Options.ElementAt(1).Value;
        var builder = new ComponentBuilder().WithButton("Example", style: ButtonStyle.Link, url: "https://example.com");
        await command.RespondAsync("" + Math.Pow(num, exp), components: builder.Build());
    }
}