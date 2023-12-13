"""Cog řešící reakce na vyvolané výjimky."""

import logging

import discord
from discord import app_commands
from discord.ext import commands


class OnError(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def cog_load(self) -> None:
        self.bot.tree.on_error = self.on_app_command_error
        self.bot.on_command_error = self.on_command_error

    # Výjimky vyvolané v rámci slash commands
    async def on_app_command_error(self, itx: discord.Interaction, error: app_commands.AppCommandError) -> None:
        is_unknown = False

        # Reagovat podle typu chyby:
        if isinstance(error, app_commands.MissingPermissions):
            # Pokud uživatel nemá dostatečná práva, informovat ho emphemeral zprávou
            content = "Pro spuštění tohoto příkazu (v této konverzaci) nemáte dostatečná práva."
            ephemeral = True
        else:
            # Pokud daná chyba není jinak specificky ošetřena, odeslat do chatu výpis chyby (červeně)
            content = f"```ansi\n[2;31m{error}```"
            ephemeral = False
            is_unknown = True

        # Použitá metoda pro odeslání reakce závisí na typu interakce:
        match itx.response.type:
            case discord.InteractionResponseType.deferred_channel_message:
                # Pokud "Bot přemýšlí"
                await itx.followup.send(content=content, ephemeral=ephemeral)  # ???: Ephemeral nefunguje u followups
            case _:
                # Ostatní případy
                await itx.response.send_message(content=content, ephemeral=ephemeral)

        # Log
        if is_unknown:
            logging.getLogger("discord").error("Ignoring exception in app_command %r", itx.command.name, exc_info=error)

    # Vyjímky vyvolané v rámci starého typu příkazů
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        is_unknown = False

        # Reagovat podle typu chyby:
        if isinstance(error, (commands.NotOwner, commands.PrivateMessageOnly)):
            # Běžný uživatel se pokouší spustit developer-only příkaz, ignorujeme
            return
        elif isinstance(error, commands.MissingPermissions):
            content = f"```ansi\n[2;33mPro spuštění tohoto příkazu (v této konverzaci) nemáte dostatečná práva.```"
        else:
            # Pokud daná chyba není jinak specificky ošetřena, odeslat do chatu výpis chyby (červeně)
            content = f"```ansi\n[2;31m{error}```"
            is_unknown = True
        await ctx.send(content=content)

        # Log
        if is_unknown:
            logging.getLogger("discord").error("Ignoring exception in command %s", ctx.command, exc_info=error)


async def setup(bot) -> None:
    await bot.add_cog(OnError(bot))
