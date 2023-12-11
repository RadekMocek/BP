import discord

import utils.db_io as database


def render_set_theme(itx: discord.Interaction, theme: database.ThemeLiteral) -> None:
    iid = __get_id_from_itx(itx)
    database.render_set_theme(iid, theme)


def render_get_theme(itx: discord.Interaction, force_user_id: bool = False) -> database.ThemeLiteral:
    if force_user_id:  # Pro tlačítka "Uložit do DMs"
        iid = itx.user.id
    else:
        iid = __get_id_from_itx(itx)
    return database.render_get_theme(iid)


def __get_id_from_itx(itx: discord.Interaction) -> int:
    if itx.guild:
        return itx.guild.id
    else:
        return itx.user.id


async def lingemod_reset(guild: discord.Guild):
    role = await guild.create_role(name="LingeMod")
    database.lingemod_reset(guild.id, role.id)
