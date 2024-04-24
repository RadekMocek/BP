"""Cog pro administraci."""

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
import utils.db_io as database
from d_modules.database_commons import lingemod_get_role, lingemod_reset, render_set_theme


class Setup(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Skupina příkazů /setup ...
    setup = app_commands.Group(name="setup", description="Změnit nastavení bota na tomto serveru.")

    @setup.command()  # /setup render_theme <theme>
    async def render_theme(self,
                           itx: discord.Interaction,
                           theme: database.ThemeLiteral) -> None:
        """
        (Admin/DM only) Nastavit barevné schéma pro vykreslování matematických výrazů.

        :param itx
        :param theme: Barevné schéma
        """
        permissions.check_admin_or_dm_only(itx)
        render_set_theme(itx, theme)
        await itx.response.send_message(content=f"Téma matematických výrazů bylo změneno na `{theme}`.", ephemeral=True)

    @setup.command()  # /setup lingemod <member>
    @app_commands.checks.has_permissions(manage_roles=True)
    async def lingemod(self, itx: discord.Interaction, member: discord.Member) -> None:
        """
        (Admin/RoleManager only) Přidat/odebrat LingeMod roli danému členovi.

        :param itx
        :param member: Člen serveru, kterému bude přidána/odebrána role LingeMod
        """
        role_id, role = lingemod_get_role(itx)
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

    # Skupina příkazů /setup permissions ...
    setup_permissions = app_commands.Group(name="permissions",
                                           description="Změnit nastavení oprávnění na tomto serveru.",
                                           parent=setup)

    # Zde by se místo dekorátoru @...checks.has_permissions(administrator=True) více hodil @...guild_only, ale:
    # "Due to a Discord limitation, this decorator does nothing in subcommands and is ignored."
    @setup_permissions.command()  # /setup permissions get
    @app_commands.checks.has_permissions(administrator=True)
    async def get(self, itx: discord.Interaction) -> None:
        """(Admin only) Vypsat aktuální nastavení oprávnění na tomto serveru."""
        await itx.response.send_message(content=f"{permissions.get_permissions_info(itx.guild.id)}", ephemeral=True)

    @setup_permissions.command()  # /setup permissions set_command <action> <permission>
    @app_commands.checks.has_permissions(administrator=True)
    async def set_command(self,
                          itx: discord.Interaction,
                          action: database.ActionCommandLiteral,
                          permission: permissions.PermissionCommandLiteral) -> None:
        """
        (Admin only) Změnit nastavení oprávnění pro příkaz na tomto serveru.

        :param itx
        :param action: Příkaz
        :param permission: Nové oprávnění pro tento příkaz
        """
        permissions.set_command_permission(itx.guild.id, action, permission)
        await itx.response.send_message(content=f"Oprávnění příkazu `{action}` bylo úspěšně změněno na `{permission}`.",
                                        ephemeral=True)

    @setup_permissions.command()  # /setup permissions set_buttons <action> <permission>
    @app_commands.checks.has_permissions(administrator=True)
    async def set_buttons(self,
                          itx: discord.Interaction,
                          action: database.ActionViewInteractionLiteral,
                          permission: permissions.PermissionViewInteractionLiteral) -> None:
        """
        (Admin only) Změnit nastavení oprávnění pro interakci s tlačítky na tomto serveru.

        :param itx
        :param action: Typ interakce
        :param permission: Nové oprávnění pro tuto interakci
        """
        permissions.set_view_interaction_permission(itx.guild.id, action, permission)
        await itx.response.send_message(
            content=f"Oprávnění interakce `{action}` bylo úspěšně změněno na `{permission}`.",
            ephemeral=True
        )

    @commands.command()  # (Starý typ příkazu, aby nerušil v našeptávači) "$> lingemod_reset"
    @commands.has_permissions(administrator=True)
    async def lingemod_reset(self, ctx: commands.Context) -> None:
        """Resetovat LingeMod roli pro daný server."""
        await lingemod_reset(ctx.guild)
        await ctx.send("Role LingeMod byla úspěšně vytvořena.")


async def setup(bot) -> None:
    await bot.add_cog(Setup(bot))
