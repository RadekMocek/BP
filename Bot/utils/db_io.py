"""Podpůrný modul pro práci s databází."""

import pathlib
import sqlite3
from typing import Any, Literal

ThemeLiteral = Literal["dark", "light", "midnight", "solar"]

ActionCommandLiteral = Literal["clear", "explain", "generate", "render"]
ActionViewInteractionLiteral = Literal["explain_btns", "generate_btns", "render_btns"]
ActionLiteral = Literal[ActionCommandLiteral, ActionViewInteractionLiteral]

DEFAULT_PERMISSIONS: dict[ActionLiteral, int] = {
    "clear": 0,
    "explain": 0,
    "explain_btns": 2,
    "generate": 0,
    "generate_btns": 2,
    "render": 0,
    "render_btns": 2
}

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


def permissions_get_all(gid: int) -> Any:
    """:return: Řádek tabulky permissions kde id serveru == gid; None pokud záznam neexistuje"""
    cursor.execute(f"SELECT * FROM permissions WHERE id=?", (gid,))
    return cursor.fetchone()


def permissions_get_one(gid: int, action: ActionLiteral) -> int:
    cursor.execute(f"SELECT {action} FROM permissions WHERE id=?", (gid,))
    return cursor.fetchone()[0]


def permissions_set(gid: int, action: ActionLiteral, permission: int) -> None:
    if not is_id_in_table(gid, "permissions"):
        cursor.execute("INSERT INTO permissions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (gid,) + tuple(DEFAULT_PERMISSIONS.values()))
    cursor.execute(f"UPDATE permissions SET {action}=? WHERE id=?", (permission, gid))
    connection.commit()


def purge_table(table_name: str) -> None:
    cursor.execute(f"DELETE FROM {table_name}")
    connection.commit()
