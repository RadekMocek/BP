"""Běžná funkcionalita pro práci nad databází."""

import discord

import utils.db_io as database


def render_set_theme(itx: discord.Interaction, theme: database.ThemeLiteral) -> None:
    """Nastavit barevného schéma pro uživatele/server s daným itx (uložit do db)"""
    iid = __get_id_from_itx(itx)
    database.render_set_theme(iid, theme)


def render_get_theme(itx: discord.Interaction, force_user_id: bool = False) -> database.ThemeLiteral:
    """Získat barevného schéma pro uživatele/server s daným itx"""
    if force_user_id:  # Pro tlačítka "Uložit do DMs"
        iid = itx.user.id
    else:
        iid = __get_id_from_itx(itx)
    return database.render_get_theme(iid)


def __get_id_from_itx(itx: discord.Interaction) -> int:
    """:return: ID uživatele/serveru s daným itx"""
    if itx.guild:
        return itx.guild.id
    else:
        return itx.user.id


async def lingemod_reset(guild: discord.Guild) -> None:
    """Znovu vytvořit roli LingeMod a aktualizovat záznam v db"""
    role = await guild.create_role(name="LingeMod")
    database.lingemod_reset(guild.id, role.id)


def lingemod_get_role(itx: discord.Interaction) -> tuple[int, discord.Role]:
    """:return: Tuple[ID LingeMod role, odpovídající discord.Role] pro dané itx"""
    role_id = database.lingemod_get_role_id(itx.guild.id)
    role = itx.guild.get_role(role_id)
    return role_id, role
