import discord
from discord import app_commands
from discord.ext import commands


class Theory(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def explain(self, itx: discord.Interaction) -> None:
        """Testovací příkaz pro zobrazení vybrané látky z teorie."""
        with open("static/01.MD", "r", encoding="utf-8") as file:
            message = file.read()
        await itx.response.send_message(message[:2000])


async def setup(bot) -> None:
    await bot.add_cog(Theory(bot))
