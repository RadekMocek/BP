"""Cog obstarávající příkazy pro příklady."""

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
from d_modules.problem_modules import ProblemView


class Problem(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def generate(self, itx: discord.Interaction) -> None:
        """Otevřít rozhraní pro generování a vysvětlení příkladů z lineární algebry."""
        permissions.command(itx, "generate")
        await itx.response.send_message("Zvolte si téma:")
        await ProblemView.attach_to_message(await itx.original_response(), itx)


async def setup(bot) -> None:
    await bot.add_cog(Problem(bot))
