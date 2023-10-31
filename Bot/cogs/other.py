import discord
from discord import app_commands
from discord.ext import commands

from utils.math_render import render_matrix_equation


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def ping(self, itx: discord.Interaction) -> None:
        """Ověřit dostupnost bota."""
        latency = round(self.bot.latency * 1000)
        await itx.response.send_message(f"Pong!\nProdleva: {latency} ms")

    @app_commands.command()
    async def help(self, itx: discord.Interaction) -> None:
        """Zobrazit nápovědu."""
        await itx.response.send_message("Nápověda.")

    @app_commands.command()
    async def render(self, itx: discord.Interaction, text: app_commands.Range[str, 1, 250]) -> None:
        """
        Vykreslit rovnici s maticemi. Podporuje základní TeX výrazy. Syntax matic podobný MATLABu.

        :param itx
        :param text: Např. "2 \\cdot [1, 2; 3, \\sqrt{4}] = [2, 4; 6, 4]"
        """
        await itx.response.defer()  # "Bot přemýšlí"
        image_buffer = render_matrix_equation(text)
        await itx.followup.send(file=discord.File(image_buffer, "texmex.png"))
        image_buffer.close()


async def setup(bot):
    await bot.add_cog(Other(bot))
