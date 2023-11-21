"""Cog řešící reakce na výjimky vyvolané v rámci slash commands."""

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
        # Reagovat podle typu chyby:
        if isinstance(error, app_commands.MissingPermissions):
            # Pokud uživatel nemá dostatečná práva, informovat ho emphemeral zprávou
            content = "Pro spuštění tohoto příkazu nemáte dostatečná práva."
            ephemeral = True
        else:
            # Pokud daná chyba není jinak specificky ošetřena, odeslat do chatu výpis chyby (červeně)
            content = f"```ansi\n[2;31m{error}```"
            ephemeral = False

        # Použitá metoda pro odeslání reakce závisí na typu interakce:
        match itx.response.type:
            case discord.InteractionResponseType.deferred_channel_message:
                # Pokud "Bot přemýšlí"
                await itx.followup.send(content=content, ephemeral=ephemeral)
            case _:
                # Ostatní případy
                await itx.response.send_message(content=content, ephemeral=ephemeral)


async def setup(bot) -> None:
    await bot.add_cog(Error(bot))
