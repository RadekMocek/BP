"""Cog pro administraci."""

import discord
from discord import app_commands
from discord.ext import commands

import modules.permissions as permissions
import utils.db_io as database


class Setup(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    setup = app_commands.Group(name="setup", description="Změnit nastavení bota na tomto serveru.")

    @setup.command()
    async def render_theme(self,
                           itx: discord.Interaction,
                           theme: database.ThemeLiteral) -> None:
        """
        (Admin/DM only) Nastavit barevné schéma pro vykreslování matematických výrazů.

        :param itx
        :param theme: Barevné schéma
        """
        permissions.admin_or_dm(itx)
        database.set_render_theme(itx, theme)
        await itx.response.send_message(content=f"Téma matematických výrazů bylo změneno na `{theme}`.", ephemeral=True)


async def setup(bot) -> None:
    await bot.add_cog(Setup(bot))
