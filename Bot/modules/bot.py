import os
import pathlib

import discord
from discord.ext import commands

from utils.file_io import json_read

__config = json_read("config.json")
TOKEN = __config["token"]
TEST_GUILD = discord.Object(id=__config["test_guild_id"])

__path_root = pathlib.Path(__file__).parent.parent
PATH_IMG = __path_root / "_img"
PATH_TEX = PATH_IMG / "tex.png"


class DisGebra(commands.Bot):
    def __init__(self):
        # Prefix pro starý typ příkazů
        command_prefix = "dg:"
        # Gateway intents určují, ke kterým událostem bude mít bot přístup
        intents = discord.Intents.default()
        intents.message_content = True  # Umožňuje botu číst zprávy
        # Status "Poslouchá /help"
        activity = discord.Activity(type=discord.ActivityType.listening, name="/help")
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            activity=activity
        )

    # Úvodní nastavení, metoda je spuštěna jednou po přihlášení
    async def setup_hook(self):
        # Nahrání cogs souborů
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} načteno.")
        # Synchronizovat slash commands
        self.tree.clear_commands(guild=TEST_GUILD)
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

    async def on_ready(self):
        print("Bot je připraven.")
