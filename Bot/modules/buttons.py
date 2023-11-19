import discord
from discord import app_commands

from modules.modals import EditMathRenderModal


class ConfirmButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="✔️", label="Potvrdit")

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.stop()
        await itx.message.edit(view=self.view.clear_items())


class EditMathRenderButton(discord.ui.Button):
    def __init__(self, text_old: app_commands.Range[str, 1, 256]) -> None:
        self.text_old = text_old
        super().__init__(emoji="📝", label="Upravit")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.response.send_modal(EditMathRenderModal(self, itx))


class DeleteButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="🗑", label="Smazat")

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.stop()
        await itx.message.delete()


class TheoryNextButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(label="Pokračovat")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.next_subtheme(itx)
