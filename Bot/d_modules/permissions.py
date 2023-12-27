from typing import Literal, Union, get_args

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

__INT_2_COMMAND: dict[int, PermissionCommandLiteral] = {
    y: x for x, y in __COMMAND_2_INT.items()
}

__VIEWINTERACTION_2_INT: dict[PermissionViewInteractionLiteral, int] = {
    "Any Admin+LingeMod": 0,
    "Any Admin": 1,
    "Author Only": 2
}

__INT_2_VIEWINTERACTION: dict[int, PermissionViewInteractionLiteral] = {
    y: x for x, y in __VIEWINTERACTION_2_INT.items()
}


def __is_admin_or_dm(itx: discord.Interaction) -> bool:
    return not itx.guild or itx.user.guild_permissions.administrator


def __get_permission(itx: discord.Interaction, action: database.ActionLiteral) -> int:
    if database.is_id_in_table(itx.guild.id, "permissions"):
        return database.permissions_get_one(itx.guild.id, action)
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


def set_command_permission(gid: int,
                           action: database.ActionCommandLiteral,
                           permission: PermissionCommandLiteral) -> None:
    database.permissions_set(gid, action, __COMMAND_2_INT[permission])


def set_view_interaction_permission(gid: int,
                                    action: database.ActionViewInteractionLiteral,
                                    permission: PermissionViewInteractionLiteral) -> None:
    database.permissions_set(gid, action, __VIEWINTERACTION_2_INT[permission])


def get_permissions_info(gid: int) -> str:
    """:return: Formátovaný řetězec informující o nastavení oprávnění na daném serveru"""
    permission_numbers = database.permissions_get_all(gid)  # Získat si oprávnění z SQLite databáze
    if not permission_numbers:  # Pokud v tabulce záznam není, server používá výchozí nastavení oprávnění
        permission_numbers = tuple(database.DEFAULT_PERMISSIONS.values())
    else:  # Pokud jsme dostali záznam z databáze, zahodit první sloupec s guild id
        permission_numbers = permission_numbers[1:]
    # Přiřadit k číslům oprávnění názvy akcí, ke kterým se vztahují; tuple tuplů (action: str, permission: int)
    permission_tuples = tuple(zip(database.DEFAULT_PERMISSIONS.keys(), permission_numbers))
    # Formátovaný výpis
    result = "".join([
        f"{__permission_info_optional_newline(x[0])}{x[0].ljust(15)}\t{__int_2_permission(x)}\n"
        for x in permission_tuples
    ])
    return f"```{result}```"


def __permission_info_optional_newline(permission_name: str) -> str:
    """Pomocná metoda pro formátovaný výpis oprávnění; má být před dalším řádkem přidán řádek prázdný?"""
    # Pokud další řádek končí na "_btns", pak se vztahuje k tomu nad ním
    if permission_name[-5:] == "_btns":
        return ""
    # jinak se jedná o novou kategorii akcí, kterou oddělíme od té předchozí prázdným řádkem
    return "\n"


def __int_2_permission(permission_tuple: tuple[str, int]) -> str:
    """
    :param permission_tuple: Tuple (action: str, permission: int)
    :return: Pojmenování pro dané oprávnění, které je na vstupu vyjádřené číslem
    """
    name, number = permission_tuple  # Podle jména akce se rozhodne, zdali se jedná o příkaz nebo interakci s View
    if name in get_args(database.ActionCommandLiteral):
        return __INT_2_COMMAND[number]
    else:
        return __INT_2_VIEWINTERACTION[number]
