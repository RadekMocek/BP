"""Tlačítka."""

import discord
from discord import app_commands

from modules.modals import EditMathRenderModal


class ConfirmButton(discord.ui.Button):
    """Tlačítko potvrzení pouze zastaví a vyčistí svůj view."""

    def __init__(self, label: str = "Potvrdit") -> None:
        super().__init__(emoji="✔️", label=label)

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.stop()
        await itx.message.edit(view=self.view.clear_items())


class EditMathRenderButton(discord.ui.Button):
    """Tlačítko editace matematického výrazu vyvolá příslušný modal."""

    def __init__(self, text_old: app_commands.Range[str, 1, 256]) -> None:
        """
        :param text_old: Aktuální text matematického výrazu, který bude předvyplněn ve vyvolaném modalu.
        """
        self.text_old = text_old
        super().__init__(emoji="📝", label="Upravit")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.response.send_modal(EditMathRenderModal(self, itx))


class DeleteButton(discord.ui.Button):
    """Tlačítko smazání zastaví svůj view a smaže zprávu, ke které je přiděleno."""

    def __init__(self) -> None:
        super().__init__(emoji="🗑", label="Smazat")

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.stop()
        await itx.message.delete()
