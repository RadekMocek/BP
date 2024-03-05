"""Obecné view komponenty."""

import logging
from typing import Any, Optional, Union

import discord

import d_modules.permissions as permissions
import utils.db_io as database
from d_modules.bot import SECRET1


# region Common Buttons
class ConfirmButton(discord.ui.Button):
    """Tlačítko potvrzení pouze zastaví a vyčistí svůj view."""

    def __init__(self, label: str = "Potvrdit") -> None:
        super().__init__(emoji="✔️", label=label)

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.stop()
        await itx.message.edit(view=self.view.clear_items())


class DeleteButton(discord.ui.Button):
    """Tlačítko smazání zastaví svůj view a smaže zprávu, ke které je přiděleno."""

    def __init__(self) -> None:
        super().__init__(emoji="🗑", label="Smazat")

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.stop()
        await itx.message.delete()


class CustomExitButton(discord.ui.Button):
    """Tlačítko volá ve svém view metodu exit, která musí být implementována."""

    def __init__(self) -> None:
        super().__init__(emoji="🚫", label="Ukončit a smazat")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.exit(itx)


class UrlGitBookButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(label="GitBook", url="https://lingebot.gitbook.io/lingebot-napoveda/")


class UrlGitHubButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(label="GitHub", url="https://github.com/RadekMocek/BP/issues")


class UrlGoogleFormsButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(label="DOTAZNÍK", url=SECRET1)


# endregion

# region Common Modals
class LingeBotModal(discord.ui.Modal):
    """Obsahuje metody/parametry společné pro všechny modaly v LingeBot."""

    async def on_error(self, itx: discord.Interaction, error: Exception) -> None:  # Log a výpis chyby do chatu
        logging.getLogger("discord").error("Ignoring exception in modal %r:", self, exc_info=error)
        await itx.followup.send(f"```ansi\n[2;31m{error}```", ephemeral=True)


# endregion

# region Common Views
class LingeBotView(discord.ui.View):
    """Obsahuje metody/parametry společné pro všechny Views v LingeBot."""

    def __init__(self,
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User],
                 timeout: float = 840):
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
        logging.getLogger("discord").error("Ignoring exception in view %r for item %r", self, item, exc_info=error)
        content = f"```ansi\n[2;31m{error}```"
        try:  # Odeslat chybové hlášení do chatu
            await itx.response.send_message(content=content)
        except discord.InteractionResponded:
            await itx.followup.send(content=content)


class MessageView(LingeBotView):
    """Základní View - kontejner pro tlačítka/selecty/textinput."""

    def __init__(self,
                 timeout: int,  # Pokud od poslední interakce uběhne tento počet vteřin, zavolá se on_timeout()
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User],
                 action: Optional[database.ActionLiteral]) -> None:
        super().__init__(timeout=timeout, parent_message=parent_message, author=author)
        self.action = action

    @classmethod
    async def attach_to_message(cls,
                                timeout: Optional[int],
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User],
                                items: list[discord.ui.Item],
                                action: Optional[database.ActionLiteral] = None) -> None:
        """Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě."""
        self = cls(timeout, parent_message, author, action)
        for item in items:
            self.add_item(item)
        await self.parent_message.edit(view=self)

    async def interaction_check(self, itx: discord.Interaction) -> bool:
        if not self.action or permissions.check_view_interaction(itx, self.author, self.action):
            return True  # Nejedná se o akci vyžadující oprávnění, nebo je má užvatel dostatečná
        # Při nedostatečných právech informovat uživatele tzv. ephemeral zprávou (zprávu vidí pouze daný uživatel)
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False
# endregion
