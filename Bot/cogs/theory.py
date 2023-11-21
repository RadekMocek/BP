"""Cog obstarávající příkazy pro výklad teorie."""

import discord
from discord import app_commands
from discord.ext import commands

from modules.theory_modules import ThemeSelect
from modules.views import MessageView


class Theory(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def explain(self, itx: discord.Interaction) -> None:
        """Otevřít rozhraní pro výklad teorie."""
        await itx.response.defer()
        await itx.followup.send("Zvolte si téma:")
        await MessageView.attach_to_message(180,
                                            await itx.original_response(),
                                            itx.user,
                                            [ThemeSelect()])


async def setup(bot) -> None:
    await bot.add_cog(Theory(bot))
