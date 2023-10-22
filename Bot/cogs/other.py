import discord
from discord import app_commands
from discord.ext import commands

from modules.bot import PATH_TEX
from utils.math_render import render_tex


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def ping(self, itx: discord.Integration):
        """Ověřit dostupnost bota."""
        latency = round(self.bot.latency * 1000)
        await itx.response.send_message(f"Pong!\nProdleva: {latency} ms")

    @app_commands.command()
    async def tex(self, itx: discord.Integration, text: app_commands.Range[str, 1, 100]):
        """
        Vykreslit TeX matematický výraz.

        :param itx: Discord interaction (akce uživatele, na kterou se reaguje)
        :param text: Matematický výraz, např. \\frac{x^2}{2}
        """
        await itx.response.send_message(f"Rendering `{text}`:")
        render_tex(text)
        with open(PATH_TEX, "rb") as fp:
            await itx.channel.send(file=discord.File(fp))


async def setup(bot):
    await bot.add_cog(Other(bot))
