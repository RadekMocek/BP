import discord
from discord import app_commands
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def cog_load(self) -> None:
        # Nastavit metodu "on_app_command_error" jako error handler pro bota
        self.bot.tree.on_error = self.on_app_command_error

    @commands.Cog.listener()
    async def on_app_command_error(self, itx: discord.Interaction, error: app_commands.AppCommandError) -> None:
        # Odeslat do chatu výpis chyby
        error_message = f"```{error}```"
        # Použitá metoda pro odeslání výpisu závisí na typu interakce:
        match itx.response.type:
            case discord.InteractionResponseType.deferred_channel_message:
                # Pokud "Bot přemýšlí"
                await itx.followup.send(error_message)
            case _:
                # Ostatní případy
                await itx.response.send_message(error_message)


async def setup(bot) -> None:
    await bot.add_cog(Error(bot))
