"""Cog pro administraci."""

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
import utils.db_io as database
from d_modules.database import render_set_theme


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
        render_set_theme(itx, theme)
        await itx.response.send_message(content=f"Téma matematických výrazů bylo změneno na `{theme}`.", ephemeral=True)

    @setup.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def lingemod(self, itx: discord.Interaction, member: discord.Member) -> None:
        """
        (Admin only) Přidat/odebrat LingeMod roli danému členovi.

        :param itx
        :param member: Člen serveru, kterému bude přidána/odebrána role LingeMod.
        """
        guild = itx.guild
        role_id = database.permissions_get_role_id(guild.id)
        role = guild.get_role(role_id)
        if role in member.roles:
            action_str = "odebrána"
        else:
            action_str = "přidána"
        await itx.response.send_message(content=f"{action_str}", ephemeral=True)


async def setup(bot) -> None:
    await bot.add_cog(Setup(bot))
