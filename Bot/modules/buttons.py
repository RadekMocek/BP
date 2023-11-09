from typing import Union

import discord
from discord import app_commands

from modules.modals import EditMathRenderModal


class Buttons(discord.ui.View):
    __TIMEOUT = 30  # Pokud od poslední interakce uběhne tento počet vteřin, zavolá se on_timeout()

    def __init__(self, parent_message: discord.Message, author: Union[discord.Member, discord.User]) -> None:
        super().__init__(timeout=self.__TIMEOUT)
        self.parent_message = parent_message
        self.author = author

    @classmethod
    async def attach_to_message(cls, parent_message: discord.Message,
                                author: Union[discord.Member, discord.User],
                                buttons: list[discord.ui.Button]) -> None:
        # Vytvořit instanci sebe sama, přidat do ní daná tlačítka a přiřadit ji k dané zprávě
        self = cls(parent_message, author)
        for button in buttons:
            self.add_item(button)
        await self.parent_message.edit(view=self)

    async def on_timeout(self) -> None:
        # Po uplynutí `__TIMEOUT` smazat sebe sama ze zprávy a přestat naslouchat interakce
        try:
            await self.parent_message.edit(view=self.clear_items())
        except discord.errors.NotFound:
            pass  # Zpráva již neexistuje
        finally:
            self.stop()

    async def interaction_check(self, itx: discord.Interaction):
        # Tlačítka může použít pouze autor původní zprávy nebo admin
        if itx.user == self.author or itx.user.guild_permissions.administrator:
            return True
        # Při nedostatečných právech informovat uživatele tzv. ephemeral zprávou (zprávu vidí pouze daný uživatel)
        await itx.response.send_message(content="Nemáte dostatečná práva pro úpravu této zprávy.", ephemeral=True)
        return False


class ConfirmBtn(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="✔️", label="Potvrdit")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.message.edit(view=self.view.clear_items())
        self.view.stop()


class EditMathRenderBtn(discord.ui.Button):
    def __init__(self, text_old: app_commands.Range[str, 1, 256]) -> None:
        self.text_old = text_old
        super().__init__(emoji="📝", label="Upravit")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.response.send_modal(EditMathRenderModal(self, itx))


class DeleteBtn(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="🗑", label="Smazat")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.message.delete()
        self.view.stop()
