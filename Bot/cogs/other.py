import discord
from discord import app_commands
from discord.ext import commands

from utils.math_render import render_tex, render_matrix


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def ping(self, itx: discord.Integration) -> None:
        """Ověřit dostupnost bota."""
        latency = round(self.bot.latency * 1000)
        await itx.response.send_message(f"Pong!\nProdleva: {latency} ms")

    @app_commands.command()
    async def tex(self, itx: discord.Integration, text: app_commands.Range[str, 1, 100]) -> None:
        """
        Vykreslit TeX matematický výraz pomocí Matplotlib Mathtext.

        :param itx
        :param text: Matematický výraz, např. \\frac{x^2}{2}
        """
        await itx.response.send_message(f"Rendering `{text}`:")
        image_buffer = render_tex(text)
        await itx.channel.send(file=discord.File(image_buffer, "tex.png"))
        image_buffer.close()

    @app_commands.command()
    async def mex(self, itx: discord.Integration, text: app_commands.Range[str, 1, 100]) -> None:
        """
        Vykreslit matici.

        :param itx
        :param text: Matice, syntax podobná MATLABu, např. [1, 2, 3; 4, 5, 6]. Podporuje i TeX výrazy.
        """
        await itx.response.send_message(f"Rendering `{text}`:")
        image_buffer = render_matrix(text)
        await itx.channel.send(file=discord.File(image_buffer, "mex.png"))
        image_buffer.close()


async def setup(bot):
    await bot.add_cog(Other(bot))
