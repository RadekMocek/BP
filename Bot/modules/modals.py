import discord
from discord import app_commands
from utils.math_render import render_matrix_equation


class EditMathRenderModal(discord.ui.Modal):
    def __init__(self, btn_itx: discord.Interaction, text_old: app_commands.Range[str, 1, 250]) -> None:
        self.btn_itx = btn_itx
        super().__init__(title="Upravit matematický výraz")
        self.add_item(discord.ui.TextInput(label="Nový výraz", default=text_old, min_length=1, max_length=250))

    async def on_submit(self, itx: discord.Interaction) -> None:
        await itx.response.send_message(f'Thanks for your response, {self.children[0].value}!', ephemeral=True)
        # image_buffer = render_matrix_equation(self.children[0].value)
        # await self.btn_itx.message.edit(file=discord.File(image_buffer, "lingebot_math_render.png"))
        # image_buffer.close()
