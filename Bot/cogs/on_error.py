"""Cog řešící reakce na vyvolané výjimky."""

import logging

import discord
from discord import app_commands
from discord.ext import commands


class OnError(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def cog_load(self) -> None:  # Nastavit metody z tohoto cog jako botovy výchozí error handlery
        self.bot.tree.on_error = self.on_app_command_error  # Slash commands error
        self.bot.on_command_error = self.on_command_error  # Starý typ příkazů

    async def on_app_command_error(self, itx: discord.Interaction, error: app_commands.AppCommandError) -> None:
        """Reaguje na výjimky vyvolané v rámci slash commands"""
        is_unknown = False  # True pokud pro tuto výjimku není připraveno specifické ošetření (pak by se měla zalogovat)
        print(error)
        print(type(error))
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
                await itx.followup.send(content=content)  # , ephemeral=ephemeral)
                # Followups nemohou být ephemeral (https://github.com/discordjs/discord.js/issues/5702)
            case _:
                # Ostatní případy
                await itx.response.send_message(content=content, ephemeral=ephemeral)

        # Logovat neočekávané výjimky
        if is_unknown:
            logging.getLogger("discord").error("Ignoring exception in app_command %r", itx.command.name, exc_info=error)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Reaguje na vyjímky vyvolané v rámci starého typu příkazů"""
        is_unknown = False  # True pokud pro tuto výjimku není připraveno specifické ošetření (pak by se měla zalogovat)

        # Reagovat podle typu chyby:
        if isinstance(error, (commands.NotOwner, commands.PrivateMessageOnly, commands.CommandNotFound)):
            # Běžný uživatel se pokouší spustit developer-only příkaz nebo příkaz neexistuje, ignorujeme
            return
        elif isinstance(error, commands.MissingPermissions):
            # Pokud uživatel nemá dostatečná práva, informovat ho
            content = f"```ansi\n[2;33mPro spuštění tohoto příkazu (v této konverzaci) nemáte dostatečná práva.```"
        else:
            # Pokud daná chyba není jinak specificky ošetřena, odeslat do chatu výpis chyby (červeně)
            content = f"```ansi\n[2;31m{error}```"
            is_unknown = True
        await ctx.send(content=content)

        # Logovat neočekávané výjimky
        if is_unknown:
            logging.getLogger("discord").error("Ignoring exception in command %s", ctx.command, exc_info=error)


async def setup(bot) -> None:
    await bot.add_cog(OnError(bot))
