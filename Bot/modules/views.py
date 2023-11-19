from typing import Union

import discord

from modules.buttons import TheoryNextButton
from utils.theory_utils import get_theme


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
        # View itemy může použít pouze autor původní zprávy nebo admin
        if itx.user == self.author or itx.user.guild_permissions.administrator:
            return True
        # Při nedostatečných právech informovat uživatele tzv. ephemeral zprávou (zprávu vidí pouze daný uživatel)
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False


class TheoryView(discord.ui.View):
    def __init__(self,
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User],
                 theme: str) -> None:
        super().__init__(timeout=None)  # Žádný timeout
        self.parent_message = parent_message
        self.author = author
        self.theme_name, self.subtheme_names, self.subtheme_texts = get_theme(theme)
        self.subtheme_index = -1

    @classmethod
    async def attach_to_message(cls,
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User],
                                theme: str) -> None:
        # Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě
        self = cls(parent_message, author, theme)
        self.add_item(TheoryNextButton())
        # Embed
        embed_description = "".join(f"{x[3:]}\n" for x in self.subtheme_names)
        embed_message = discord.Embed(title=self.theme_name, description=embed_description)
        await self.parent_message.edit(content="", view=self, embed=embed_message)

    async def interaction_check(self, itx: discord.Interaction):
        # View itemy může použít pouze autor původní zprávy nebo admin
        if itx.user == self.author or itx.user.guild_permissions.administrator:
            return True
        # Při nedostatečných právech informovat uživatele ephemeral zprávou
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False

    async def next_subtheme(self, itx: discord.Interaction) -> None:
        self.subtheme_index += 1
        index = self.subtheme_index
        message_content = (self.subtheme_names[index] + self.subtheme_texts[index])[:2000]
        await self.parent_message.delete()
        await itx.response.send_message(content=f"{message_content}", view=self)
        self.parent_message = await itx.original_response()
