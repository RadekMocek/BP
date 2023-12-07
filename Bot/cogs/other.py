"""Cog obstarávající ostatní nezařezené příkazy."""

import io

import discord
from discord import app_commands
from discord.ext import commands

from modules.common_modules import ConfirmButton, DeleteButton, MessageView
from modules.other_modules import EditMathRenderButton
from utils.math_render import render_matrix_equation_align_to_buffer


class Other(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def ping(self, itx: discord.Interaction) -> None:
        """Ověřit dostupnost bota."""
        latency = round(self.bot.latency * 1000)
        await itx.response.send_message(f"Pong!\nProdleva: {latency} ms")

    @app_commands.command()
    # @app_commands.checks.has_permissions(administrator=True)
    async def clear(self, itx: discord.Interaction) -> None:
        """Poslat dlouhou prázdnou zprávu (admin only)."""
        if itx.guild and not itx.user.guild_permissions.administrator:
            raise discord.app_commands.MissingPermissions(["Není admin."])
        await itx.response.send_message("⠀\n" * 45)

    @app_commands.command()
    async def help(self, itx: discord.Interaction) -> None:
        """Zobrazit nápovědu."""
        await itx.response.send_message("Nápověda.")

    @app_commands.command()
    async def render(self, itx: discord.Interaction, text: app_commands.Range[str, 1, 256]) -> None:
        """
        Vykreslit matematický výraz. Podporuje základní TeX výrazy. Syntax matic podobný MATLABu.

        :param itx
        :param text: Např. "2 \\cdot [1, 2; 3, \\sqrt{4}] = [2, 4; 6, 4]"
        """
        # Po zavolání defer Discord napíše, že "Bot přemýšlí", followup s odpovědí může pak být odeslán později
        await itx.response.defer()
        # Byte buffer, do kterého bude vložen obrázek s vykresleným matematickým výrazem
        image_buffer = io.BytesIO()
        # Pokusit se výraz vykreslit, případně odpovědět chybovým hlášením
        try:
            render_matrix_equation_align_to_buffer(image_buffer, text)
            await itx.followup.send(file=discord.File(image_buffer, "lingebot_math_render.png"))
        except ValueError as error:
            await itx.followup.send(f"```{error}```")
        finally:
            image_buffer.close()
        # Přidat ke zprávě tlačítka
        await MessageView.attach_to_message(30,
                                            await itx.original_response(),
                                            itx.user,
                                            [ConfirmButton(), EditMathRenderButton(text), DeleteButton()])


async def setup(bot) -> None:
    await bot.add_cog(Other(bot))
