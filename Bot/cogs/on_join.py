"""Cog obstarává: Pokud se bot připojí na nový server, vytvoří na něm roli pro LingeBot moderátory."""

import discord
from discord.ext import commands

import utils.db_io as database


class OnJoin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def cog_load(self) -> None:
        self.bot.on_guild_join = self.on_guild_join

    async def on_guild_join(self, guild: discord.Guild) -> None:
        role = await guild.create_role(name="LingeMod")
        database.permissions_reset(guild.id, role.id)


async def setup(bot) -> None:
    await bot.add_cog(OnJoin(bot))
