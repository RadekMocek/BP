import discord
from discord import app_commands

from modules.modals import EditMathRenderModal


class Buttons(discord.ui.View):
    __TIMEOUT = 30

    def __init__(self, parent_message: discord.Message) -> None:
        super().__init__(timeout=self.__TIMEOUT)
        self.parent_message = parent_message

    @classmethod
    async def attach_to_message(cls, parent_message: discord.Message, buttons: list[discord.ui.Button]) -> None:
        self = cls(parent_message)
        for button in buttons:
            self.add_item(button)
        await self.parent_message.edit(view=self)

    async def on_timeout(self) -> None:
        try:
            await self.parent_message.edit(view=self.clear_items())
        except discord.errors.NotFound:
            pass
        finally:
            self.stop()


class ConfirmBtn(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="✔️", label="Potvrdit")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.message.edit(view=self.view.clear_items())
        self.view.stop()


class EditMathRenderBtn(discord.ui.Button):
    def __init__(self, text_old: app_commands.Range[str, 1, 250]) -> None:
        self.text_old = text_old
        super().__init__(emoji="📝", label="Upravit")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.response.send_modal(EditMathRenderModal(itx, self.text_old))


class DeleteBtn(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="🗑", label="Smazat")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.message.delete()
        self.view.stop()
