"""Cog pro administraci."""

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
import utils.db_io as database
from d_modules.database_commons import lingemod_reset, render_set_theme


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
        role_id = database.lingemod_get_role_id(guild.id)
        role = guild.get_role(role_id)
        if role_id == -1 or not role:
            await itx.response.send_message(
                content="LingeMod role nebyla nalezena.\n"
                        "Napsáním `$> lingemod_reset` do chatu ji znovu vytvoříte (admin only).",
                ephemeral=True)
            return
        if role in member.roles:
            action_str = "odebrána"
            await member.remove_roles(role)
        else:
            action_str = "přidána"
            await member.add_roles(role)
        await itx.response.send_message(content=f"Role `{role}` byla {action_str} uživateli `{member}`.",
                                        ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lingemod_reset(self, ctx: commands.Context) -> None:
        """Resetovat LingeMod roli pro daný server."""
        await lingemod_reset(ctx.guild)
        await ctx.send("Role LingeMod byla úspěšně vytvořena.")


async def setup(bot) -> None:
    await bot.add_cog(Setup(bot))
