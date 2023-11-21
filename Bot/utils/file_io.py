"""Podpůrný modul pro zápis/čtení ze souborů. Momentálně pouze pro načtení konfigurace z JSON souboru."""

import json


def json_read(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)
