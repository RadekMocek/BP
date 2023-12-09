"""Podpůrný modul pro zápis/čtení ze souborů. (Načtení konfigurace z JSON souboru nebo teorie/tutorial z MD souborů)."""

import json
from typing import Optional


def json_read(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)


def txt_read(path) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None  # Vrátit prázdný string, pokud soubor neexistuje
