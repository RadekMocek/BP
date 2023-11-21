"""Hlavní modul – bot samotný."""

import os

import discord
from discord.ext import commands

from utils.file_io import json_read

__config = json_read("config.json")
TOKEN = __config["token"]  # Botův ověřovací token pro komunikaci s Discord API
TEST_GUILD = discord.Object(id=__config["test_guild_id"])  # Id testovacího serveru


class LingeBot(commands.Bot):
    def __init__(self) -> None:
        # Prefix pro starý typ příkazů
        command_prefix = "$> "
        # Gateway intents určují, ke kterým událostem bude mít bot přístup
        intents = discord.Intents.default()
        intents.message_content = True  # Umožňuje botu číst zprávy
        # Status "Poslouchá /help"
        activity = discord.Activity(type=discord.ActivityType.listening, name="/help")
        # LingeBot dědí od obecného bota
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            activity=activity
        )

    # Úvodní nastavení, metoda je spuštěna jednou po přihlášení
    async def setup_hook(self) -> None:
        # Nahrání cogs souborů
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} načteno.")
        # Synchronizovat slash commands na testovacím serveru
        # self.tree.clear_commands(guild=TEST_GUILD)
        # await self.tree.sync(guild=TEST_GUILD)

    async def on_ready(self) -> None:
        print("Bot je připraven.")
