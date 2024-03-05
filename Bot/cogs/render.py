"""Cog obstarávající příkaz /render pro vykreslení libovolného matematického výrazu."""

import io

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
from d_modules.common_modules import ConfirmButton, DeleteButton, MessageView
from d_modules.database_commons import render_get_theme
from d_modules.render_modules import EditMathRenderButton
from utils.math_render import render_matrix_equation_align_to_buffer


class Render(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def render(self, itx: discord.Interaction, text: app_commands.Range[str, 1, 1024]) -> None:
        """
        Vykreslit matematický výraz. Podporuje základní TeX výrazy. Syntax matic podobný MATLABu.

        :param itx
        :param text: Např. "2 \\cdot [1, 2; 3, \\sqrt{4}] = [2, 4; 6, 4]"
        """
        # Zkontrolovat, zdali má uživatel na daném serveru oprávnění tento příkaz použít
        permissions.check_command(itx, "render")
        # Po zavolání defer Discord napíše, že "Bot přemýšlí", followup s odpovědí může pak být odeslán později
        await itx.response.defer()
        # Byte buffer, do kterého bude vložen obrázek s vykresleným matematickým výrazem
        image_buffer = io.BytesIO()
        # Pokusit se výraz vykreslit, případně odpovědět chybovým hlášením
        render_theme_name = render_get_theme(itx)  # Získat si barevné schéma odpovídající aktuálnímu serveru/uživateli
        try:
            render_matrix_equation_align_to_buffer(image_buffer, text, render_theme_name)
            await itx.followup.send(file=discord.File(image_buffer, "lingebot_math_render.png"))
        except ValueError as error:
            await itx.followup.send(f"```{error}```")
        finally:
            image_buffer.close()
        # Přidat ke zprávě tlačítka
        await MessageView.attach_to_message(30,
                                            await itx.original_response(),
                                            itx.user,
                                            [ConfirmButton(),
                                             EditMathRenderButton(text, render_theme_name),
                                             DeleteButton()],
                                            "render_btns")


async def setup(bot) -> None:
    await bot.add_cog(Render(bot))
