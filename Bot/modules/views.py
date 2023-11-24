"""Views."""

import logging
from typing import Any, Optional, Union

import discord


class LingeBotView(discord.ui.View):
    """Obsahuje metody/parametry společné pro všechny Views v LingeBot."""

    def __init__(self,
                 timeout: Optional[float],
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User]):
        super().__init__(timeout=timeout)
        self.parent_message = parent_message
        self.author = author

    async def on_timeout(self) -> None:
        # Po uplynutí timeout smazat sebe sama ze zprávy a přestat naslouchat interakce
        try:
            await self.parent_message.edit(view=self.clear_items())
        except discord.errors.NotFound:
            pass  # Zpráva již neexistuje
        finally:
            self.stop()

    async def on_error(self, itx: discord.Interaction, error: Exception, item: discord.ui.Item[Any]) -> None:
        logging.getLogger("discord").error('Ignoring exception in view %r for item %r', self, item, exc_info=error)
        content = f"```ansi\n[2;31m{error}```"
        try:
            await itx.response.send_message(content=content)
        except discord.InteractionResponded:
            await itx.followup.send(content=content)


class MessageView(LingeBotView):
    def __init__(self,
                 timeout: int,  # Pokud od poslední interakce uběhne tento počet vteřin, zavolá se on_timeout()
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User]) -> None:
        super().__init__(timeout=timeout, parent_message=parent_message, author=author)

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

    async def interaction_check(self, itx: discord.Interaction) -> bool:
        # View itemy může použít pouze autor původní zprávy nebo admin
        if itx.user == self.author or itx.user.guild_permissions.administrator:
            return True
        # Při nedostatečných právech informovat uživatele tzv. ephemeral zprávou (zprávu vidí pouze daný uživatel)
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False
