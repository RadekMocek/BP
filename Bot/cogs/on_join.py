"""Cog obstarává: Pokud se bot připojí na nový server, vytvoří na něm roli pro LingeBot moderátory."""

import discord
from discord.ext import commands

from d_modules.database_commons import permissions_reset


class OnJoin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def cog_load(self) -> None:
        self.bot.on_guild_join = self.on_guild_join

    async def on_guild_join(self, guild: discord.Guild) -> None:
        await permissions_reset(guild)


async def setup(bot) -> None:
    await bot.add_cog(OnJoin(bot))
