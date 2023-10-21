import os

import discord
from discord.ext import commands

from Bot.utils.file_io import json_read

__config = json_read("config.json")
TOKEN = __config["token"]
TEST_GUILD = discord.Object(id=__config["test_guild_id"])


class DisGebra(commands.Bot):
    def __init__(self):
        command_prefix = "dg:"
        intents = discord.Intents.default()
        intents.message_content = True
        activity = discord.Activity(type=discord.ActivityType.listening, name="/help")
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            activity=activity
        )

    async def setup_hook(self):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} načteno.")
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

    async def on_ready(self):
        print("Bot je připraven.")
