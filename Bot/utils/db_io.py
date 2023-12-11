"""Podpůrný modul pro práci s databází."""

import pathlib
import sqlite3
from typing import Literal

import discord

ThemeLiteral = Literal["dark", "light", "midnight", "solar"]

path = pathlib.Path(__file__).parent.parent / "_database"
db_file = path / "database.db"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()


def set_render_theme(itx: discord.Interaction, theme: ThemeLiteral) -> None:
    iid = __get_id_from_itx(itx)
    exists = __is_id_in_table(iid, "render")
    if exists:
        cursor.execute("UPDATE render SET theme=? WHERE id=?", (theme, iid))
    else:
        cursor.execute("INSERT INTO render VALUES (?, ?)", (iid, theme))
    connection.commit()


def get_render_theme(itx: discord.Interaction, force_user_id: bool = False) -> ThemeLiteral:
    if force_user_id:  # Pro tlačítka "Uložit do DMs"
        iid = itx.user.id
    else:
        iid = __get_id_from_itx(itx)
    exists = __is_id_in_table(iid, "render")
    if exists:
        cursor.execute("SELECT theme FROM render WHERE id=?", (iid,))
        return cursor.fetchone()[0]
    return "dark"


def purge():
    cursor.execute("DELETE FROM render")
    cursor.execute("DELETE FROM permissions")
    connection.commit()


def __get_id_from_itx(itx: discord.Interaction) -> int:
    if itx.guild:
        return itx.guild.id
    else:
        return itx.user.id


def __is_id_in_table(iid: int, table_name: str) -> bool:
    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE id=?)", (iid,))
    exists = cursor.fetchone()
    return exists[0] == 1
