from typing import Literal, Union

import discord

import utils.db_io as database
from d_modules.database_commons import lingemod_get_role

PermissionCommandLiteral = Literal["Anyone", "Admin+LingeMod Only", "Admin Only"]
PermissionViewInteractionLiteral = Literal["Any Admin+LingeMod", "Any Admin", "Author Only"]

__COMMAND_2_INT: dict[PermissionCommandLiteral, int] = {
    "Anyone": 0,
    "Admin+LingeMod Only": 1,
    "Admin Only": 2
}

__VIEWINTERACTION_2_INT: dict[PermissionViewInteractionLiteral, int] = {
    "Any Admin+LingeMod": 0,
    "Any Admin": 1,
    "Author Only": 2
}


def __is_admin_or_dm(itx: discord.Interaction) -> bool:
    return not itx.guild or itx.user.guild_permissions.administrator


def __get_permission(itx: discord.Interaction, action: database.ActionLiteral) -> int:
    if database.is_id_in_table(itx.guild.id, "permissions"):
        return database.permissions_get(itx.guild.id, action)
    else:
        return database.DEFAULT_PERMISSIONS[action]  # Pokud oprávnění nenajdeme v databázi, použijeme ta defaultní


def admin_or_dm_only(itx: discord.Interaction) -> None:
    if not __is_admin_or_dm(itx):
        raise discord.app_commands.MissingPermissions(["Nedostatečná práva."])


def command(itx: discord.Interaction, action: database.ActionLiteral) -> None:
    if not __check_command(itx, action):
        raise discord.app_commands.MissingPermissions(["Nedostatečná práva."])


def __check_command(itx: discord.Interaction, action: database.ActionLiteral) -> bool:
    # Pokud je uživatel admin, nebo se nacházíme v DMs, spuštění příkazu je vždy povoleno
    if __is_admin_or_dm(itx):
        return True
    # Jinak je třeba zjistit, jaká oprávnění jsou pro daný příkaz na daném serveru nastavena
    permission = __get_permission(itx, action)
    # Příkaz je dostupný všem
    if permission == 0:
        return True
    # Již víme, že user není admin
    if permission == 2:
        return False
    # Pokud se jedná o Admin/LingeMod only příkaz (a víme, že user není admin), musíme ověřit roli usera
    role_id, role = lingemod_get_role(itx)
    return role_id != -1 and role and role in itx.user.roles


def view_interaction(itx: discord.Interaction,
                     view_author: Union[discord.Member, discord.User],
                     action: database.ActionLiteral) -> bool:
    # Původní uživatel podpůrného příkazu, který view vyvolal, s ním může vždy interagovat
    if itx.user == view_author:
        return True
    # Jinak je třeba zjistit, jaká oprávnění jsou pro danou view interakci na daném serveru nastavena
    permission = __get_permission(itx, action)
    # Již víme, že uživatel není "autorem" daného view
    if permission == 2:
        return False
    # Admin
    if itx.user.guild_permissions.administrator and permission < 2:
        return True
    # Mod
    if permission == 0:
        role_id, role = lingemod_get_role(itx)
        return role_id != -1 and role and role in itx.user.roles
    return False


def set_permission():
    pass  # TODO
