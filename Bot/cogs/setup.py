"""Cog pro administraci."""

from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    setup = app_commands.Group(name="setup", description="(Admin/DM only) Změnit nastavení bota na tomto serveru.")

    @setup.command()
    async def render_theme(self,
                           itx: discord.Interaction,
                           theme: Literal["dark", "light", "midnight", "solar"]) -> None:
        """
        (Admin/DM only) Nastavit barevné schéma pro vykreslování matematických výrazů.

        :param itx
        :param theme: Barevné schéma
        """
        await itx.response.send_message(content=f"Zvolené téma: {theme}.", ephemeral=True)


async def setup(bot) -> None:
    await bot.add_cog(Setup(bot))
