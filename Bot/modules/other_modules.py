"""Ostatní view komponenty."""

import io

import discord
from discord import app_commands

from modules.common_modules import LingeBotModal
from utils.math_render import render_matrix_equation_align_to_buffer


# region Other Buttons
class EditMathRenderButton(discord.ui.Button):
    """Tlačítko editace matematického výrazu vyvolá příslušný modal."""

    def __init__(self, text_old: app_commands.Range[str, 1, 1024]) -> None:
        """
        :param text_old: Aktuální text matematického výrazu, který bude předvyplněn ve vyvolaném modalu.
        """
        self.text_old = text_old
        super().__init__(emoji="📝", label="Upravit")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.response.send_modal(EditMathRenderModal(self, itx))


# endregion

# region Other Modals
class EditMathRenderModal(LingeBotModal):
    """Modal pro editaci matematického výrazu."""

    def __init__(self, button, itx: discord.Interaction) -> None:
        """
        :param button: Tlačítko, které vyvolalo tento modal
        :param itx: Interakce vyvolaná stisknutím tlačítka button
        """
        self.button = button
        self.itx = itx
        super().__init__(title="Upravit matematický výraz")
        self.add_item(discord.ui.TextInput(label="Nový výraz",
                                           default=self.button.text_old,
                                           min_length=1,
                                           max_length=1024))

    async def on_submit(self, itx: discord.Interaction) -> None:
        await itx.response.defer()  # "Modal přemýšlí"

        text = self.children[0].value  # Hodnota textového pole – nový matematický výraz
        message = self.itx.message  # Zpráva, které náleží tlačítko, jež vyvolalo tento modal

        # Vykreslit nový obrázek podle nového matematického výrazu:
        image_buffer = io.BytesIO()
        try:
            # Nahradit obrázek u zprávy. Smazat text zprávy, pokud zde nějaký byl (error message)
            render_matrix_equation_align_to_buffer(image_buffer, text)
            await message.edit(content=None, attachments=[discord.File(image_buffer, "lingebot_math_render.png")])
        except ValueError as error:
            # Vypsat chybu. Smazat starý obrázek, pokud zde nějaký byl.
            await message.edit(content=f"```{error}```", attachments=[])
        finally:
            image_buffer.close()

        # Předat nový matematický výraz zpět tlačítku, aby mohl být při případném
        # dalším otevření tohoto modalu nastaven jako defaultní hodnota textového pole.
        self.button.text_old = text

# endregion
