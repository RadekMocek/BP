import discord

import utils.db_io as database


def __is_admin_or_dm(itx: discord.Interaction):
    return itx.user.guild_permissions.administrator or not itx.guild


def admin_or_dm_only(itx: discord.Interaction):
    if not __is_admin_or_dm(itx):
        raise discord.app_commands.MissingPermissions(["Nedostatečná práva."])


__DEFAULT_PERMISSIONS: dict[database.ActionLiteral, int] = {
    "clear": 1,
    "explain": 1,
    "explain_btns": 2,
    "generate": 1,
    "generate_btns": 2,
    "render": 0,
    "render_btns": 2
}


async def command(itx: discord.Interaction, action: database.ActionLiteral):
    if not __check_command(itx, action):
        raise discord.app_commands.MissingPermissions(["Nedostatečná práva."])


def __check_command(itx: discord.Interaction, action: database.ActionLiteral) -> bool:
    # Pokud je uživatel admin, nebo se nacházíme v DMs, spuštění příkazu je vždy povoleno
    if __is_admin_or_dm(itx):
        return True
    # Jinak je třeba zjistit, jaká oprávnění jsou pro daný příkaz na daném serveru nastavena
    if database.is_id_in_table(itx.guild.id, "permissions"):
        permission = database.permissions_get(itx.guild.id, action)
    else:
        permission = __DEFAULT_PERMISSIONS[action]  # Pokud oprávnění nenajdeme v databázi, použijeme ta defaultní
    # Příkaz je dostupný všem
    if permission == 0:
        return True
    # Již víme, že user není admin
    elif permission == 2:
        return False
    # Pokud se jedná o Admin/LingeMod only příkaz (a víme, že user není admin), musíme ověřit roli usera
    role_id = database.lingemod_get_role_id(itx.guild.id)
    role = itx.guild.get_role(role_id)
    return role_id != -1 and role and role in itx.user.roles
