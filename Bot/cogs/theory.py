"""Cog obstarávající příkazy pro výklad teorie."""

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
from d_modules.common_modules import MessageView
from d_modules.theory_modules import TheoryThemeSelect


class Theory(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def explain(self, itx: discord.Interaction) -> None:
        """Otevřít rozhraní pro výklad teorie."""
        permissions.check_command(itx, "explain")
        await itx.response.send_message("Zvolte si téma:")
        await MessageView.attach_to_message(840,
                                            await itx.original_response(),
                                            itx.user,
                                            [TheoryThemeSelect()],
                                            "explain_btns")


async def setup(bot) -> None:
    await bot.add_cog(Theory(bot))
