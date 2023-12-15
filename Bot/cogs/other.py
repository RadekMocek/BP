"""Cog obstarávající ostatní nezařezené příkazy."""

import platform

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions


class Other(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def clear(self, itx: discord.Interaction) -> None:
        """Poslat dlouhou prázdnou zprávu (admin only)."""
        permissions.command(itx, "clear")
        await itx.response.send_message("⠀\n" * 45)

    @app_commands.command()
    async def help(self, itx: discord.Interaction) -> None:
        """Zobrazit nápovědu."""
        await itx.response.send_message("Nápověda.")

    @app_commands.command()
    async def ping(self, itx: discord.Interaction) -> None:
        """Ověřit dostupnost bota."""
        embed_message = discord.Embed(title="Pong!", description=(
            f"```Prodleva         {round(self.bot.latency * 1000)} ms```"
            f"```Uptime           {self.bot.get_uptime()}```"
            f"```Pčt. serverů     {len(self.bot.guilds)}```"
            f"```Python verze     {platform.python_version()}```"
            f"```OS               {platform.system()} {platform.release()}```"
        ))
        await itx.response.send_message(embed=embed_message, ephemeral=True)


async def setup(bot) -> None:
    await bot.add_cog(Other(bot))
