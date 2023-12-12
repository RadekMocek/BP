"""Podpůrný modul pro práci s databází."""

import pathlib
import sqlite3
from typing import Literal

ThemeLiteral = Literal["dark", "light", "midnight", "solar"]
ActionLiteral = Literal["clear", "explain", "explain_btns", "generate", "generate_btns", "render", "render_btns"]

path = pathlib.Path(__file__).parent.parent / "_database"
db_file = path / "database.db"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()


def is_id_in_table(iid: int, table_name: str) -> bool:
    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE id=?)", (iid,))
    exists = cursor.fetchone()
    return exists[0] == 1


def render_set_theme(iid: int, theme: ThemeLiteral) -> None:
    exists = is_id_in_table(iid, "render")
    if exists:
        cursor.execute("UPDATE render SET theme=? WHERE id=?", (theme, iid))
    else:
        cursor.execute("INSERT INTO render VALUES (?, ?)", (iid, theme))
    connection.commit()


def render_get_theme(iid: int) -> ThemeLiteral:
    exists = is_id_in_table(iid, "render")
    if exists:
        cursor.execute("SELECT theme FROM render WHERE id=?", (iid,))
        return cursor.fetchone()[0]
    return "dark"


def lingemod_reset(gid: int, role_id: int) -> None:
    if is_id_in_table(gid, "lingemod"):
        cursor.execute("DELETE FROM lingemod WHERE id=?", (gid,))
    cursor.execute("INSERT INTO lingemod VALUES (?, ?)", (gid, role_id))
    connection.commit()


def lingemod_get_role_id(gid: int) -> int:
    """
    :param gid: ID Discord serveru
    :return: ID LingeMod role na daném serveru. Pokud záznam neexistuje, vrací -1.
    """
    cursor.execute("SELECT role_id FROM lingemod WHERE id=?", (gid,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return -1


def permissions_get(gid: int, action: ActionLiteral) -> int:
    cursor.execute(f"SELECT {action} FROM permissions WHERE id=?", (gid,))
    return cursor.fetchone()[0]


def purge_table(table_name: str):
    cursor.execute(f"DELETE FROM {table_name}")
    connection.commit()
