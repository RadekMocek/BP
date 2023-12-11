"""Inicializace databáze pro bota."""

import pathlib
import sqlite3

if __name__ == "__main__":
    path = pathlib.Path(__file__).parent / "_database"
    path.mkdir(exist_ok=True)
    db_file = path / "database.db"
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS render(id, theme)")
    cursor.execute("CREATE TABLE IF NOT EXISTS lingemod(id, role_id)")
    cursor.execute("CREATE TABLE IF NOT EXISTS permissions(id, clear, explain, explain_btns, generate, generate_btns, render, render_btns)")
