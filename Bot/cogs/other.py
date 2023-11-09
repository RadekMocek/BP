import io

import discord
from discord import app_commands
from discord.ext import commands

from modules.buttons import Buttons, ConfirmBtn, EditMathRenderBtn, DeleteBtn
from utils.math_render import render_matrix_equation_to_buffer


class Other(commands.Cog):
    def __init__(self, bot) -> None:
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
    async def render(self, itx: discord.Interaction, text: app_commands.Range[str, 1, 256]) -> None:
        """
        Vykreslit matematický výraz. Podporuje základní TeX výrazy. Syntax matic podobný MATLABu.

        :param itx
        :param text: Např. "2 \\cdot [1, 2; 3, \\sqrt{4}] = [2, 4; 6, 4]"
        """
        await itx.response.defer()  # "Bot přemýšlí"

        image_buffer = io.BytesIO()

        try:
            render_matrix_equation_to_buffer(image_buffer, text)
            await itx.followup.send(file=discord.File(image_buffer, "lingebot_math_render.png"))
        except ValueError as error:
            await itx.followup.send(f"```{error}```")
        finally:
            image_buffer.close()

        await Buttons.attach_to_message(await itx.original_response(),
                                        itx.user,
                                        [ConfirmBtn(), EditMathRenderBtn(text), DeleteBtn()])


async def setup(bot) -> None:
    await bot.add_cog(Other(bot))
