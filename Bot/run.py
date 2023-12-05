"""Modul nastaví logování a spustí bota."""

import logging
import pathlib
from logging.handlers import RotatingFileHandler

from modules.bot import LingeBot, TOKEN

if __name__ == "__main__":
    # Upravit nastavení logování (přidat logování do souboru)
    # - Složka pro log soubory
    pathlib.Path("_logs").mkdir(exist_ok=True)
    # - https://discordpy.readthedocs.io/en/stable/logging.html
    file_handler = RotatingFileHandler(
        filename="_logs/discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    file_handler.setLevel(logging.WARNING)
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    file_handler.setFormatter(formatter)
    # - Přidat file_handler k výchozímu loggeru knihovny
    logger = logging.getLogger("discord")
    logger.addHandler(file_handler)

    # Spustit bota
    bot = LingeBot()
    bot.run(token=TOKEN, reconnect=True)
