import discord


def admin_or_dm(itx: discord.Interaction):
    if itx.guild and not itx.user.guild_permissions.administrator:
        raise discord.app_commands.MissingPermissions(["Nedostatečná práva."])
