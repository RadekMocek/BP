import discord

from utils.math_render import render_matrix_equation


class EditMathRenderModal(discord.ui.Modal):
    def __init__(self, btn, btn_itx: discord.Interaction) -> None:
        self.btn = btn
        self.btn_itx = btn_itx
        super().__init__(title="Upravit matematický výraz")
        self.add_item(discord.ui.TextInput(label="Nový výraz", default=btn.text_old, min_length=1, max_length=250))

    async def on_submit(self, itx: discord.Interaction) -> None:
        await itx.response.defer()  # "Modal přemýšlí"

        text = self.children[0].value  # Hodnota textového pole – nový matematický výraz
        message = self.btn_itx.message  # Zpráva, které náleží tlačítko, jež vyvolalo tento modal

        image_buffer = render_matrix_equation(text)  # Vykreslit nový obrázek podle nov.mat.výrazu

        # Předat nový matematický výraz zpět tlačítku, aby mohl být při případném
        # dalším otevření tohoto modalu nastaven jako defaultní hodnota textového pole.
        self.btn.text_old = text

        # Nahradit obrázek u zprávy
        await message.edit(attachments=[discord.File(image_buffer, "lingebot_math_render.png")])

        image_buffer.close()

    async def on_error(self, itx: discord.Interaction, error: Exception) -> None:
        await itx.followup.send("Chybně zadaný výraz.", ephemeral=True)
