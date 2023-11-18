from typing import Union

import discord


class MessageView(discord.ui.View):
    def __init__(self,
                 timeout: int,  # Pokud od poslední interakce uběhne tento počet vteřin, zavolá se on_timeout()
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User]) -> None:
        super().__init__(timeout=timeout)
        self.parent_message = parent_message
        self.author = author

    @classmethod
    async def attach_to_message(cls,
                                timeout: int,
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User],
                                items: list[discord.ui.Item]) -> None:
        # Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě
        self = cls(timeout, parent_message, author)
        for item in items:
            self.add_item(item)
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
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False
