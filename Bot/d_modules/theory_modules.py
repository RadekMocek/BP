"""Tlačítka, selecty, views užívaná při výkladu teorie."""

import io
from typing import Optional, Union

import discord

import d_modules.permissions as permissions
import utils.db_io as database
from d_modules.common_modules import ConfirmButton, CustomExitButton, LingeBotView, MessageView
from d_modules.database_commons import render_get_theme
from d_modules.messages import delete_messages, send_messages, try_dm_user
from utils.text_utils import raw_text_2_message_text
from utils.theory_utils import get_theme, list_themes


# region Theory Buttons
class TheorySubthemeNextButton(discord.ui.Button):
    """Tlačítko pro zobrazení dalšího podtématu aktuálně zvoleného tématu."""

    def __init__(self) -> None:
        super().__init__(emoji="➡️", label="Další")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.next_subtheme(itx)


class TheorySubthemePreviousButton(discord.ui.Button):
    """Tlačítko pro zobrazení předchozího podtématu aktuálně zvoleného tématu."""

    def __init__(self) -> None:
        super().__init__(emoji="⬅️", label="Předchozí", disabled=True)

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.previous_subtheme(itx)


class TheorySubthemeSaveButton(discord.ui.Button):
    """Tlačítko pro přeposlání aktuálně zobrazovaného podtématu do přímých zpráv."""

    def __init__(self) -> None:
        super().__init__(emoji="📨", label="Uložit do DMs", disabled=True, custom_id="SubthemeSaveButton")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.fwd_subtheme(itx)


# endregion

# region Theory Selects
class TheoryThemeSelect(discord.ui.Select):
    """Nabízí dostupná teoretická témata a po výběru vytvoří zprávu s ThemeView."""

    def __init__(self) -> None:
        options = []
        themes = list_themes()
        for theme in themes:
            options.append(discord.SelectOption(label=theme))
        super().__init__(placeholder="Zvolte si téma", min_values=1, max_values=1, options=options)

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.stop()
        chosen_theme = self.values[0]
        await itx.response.send_message(content=f"Nahrávám {chosen_theme} ...")
        await TheoryThemeView.attach_to_message(await itx.original_response(),
                                                itx,
                                                chosen_theme)
        await itx.message.delete()


class TheorySubthemeSelect(discord.ui.Select):
    """Výběr podtémat, alternativa pro `SubthemeNextButton` a `SubthemePreviousButton`."""

    def __init__(self, subthemes: list[str]) -> None:
        options = []
        for subtheme in subthemes:
            options.append(discord.SelectOption(label=subtheme))
        super().__init__(placeholder="Zvolte si podtéma nebo využijte tlačítek",
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, itx: discord.Interaction) -> None:
        chosen_subtheme = self.values[0]
        await self.view.select_subtheme(itx, chosen_subtheme)


# endregion

# region Theory Views
class TheoryThemeView(LingeBotView):
    """Poskytuje uživateli funkcionalitu pro výklad teorie."""

    def __init__(self,
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User],
                 theme: str,
                 guild: Optional[discord.Guild],
                 render_theme_name: database.ThemeLiteral) -> None:
        super().__init__(parent_message=parent_message, author=author)
        # Pokud je None, view se nachází v přímých zprávách a není třeba používat tlačítko pro přeposlání
        self.guild = guild
        # Z utils.theory_utils získat název tématu a názvy+texty podtémat
        self.theme_name, self.subtheme_names, self.subtheme_texts = get_theme(theme)
        # Index právě zobrazovaného podtématu; začíná se na "úvodní obrazovce", proto -1 (mimo rozsah)
        self.subtheme_index = -1
        # Všechny zprávy použité pro vypsání  aktuálního podtématu uloženy v listu, aby mohli smazány, až bude třeba
        self.subtheme_messages: list[discord.Message] = [parent_message]
        # Na tato tlačítka si držet referenci, aby mohly být měněny jejich parametry (disabled) dle potřeby
        self.subtheme_select = TheorySubthemeSelect(self.subtheme_names)
        self.previous_button = TheorySubthemePreviousButton()
        self.next_button = TheorySubthemeNextButton()
        self.save_button = TheorySubthemeSaveButton()
        # Barevné schéma vykreslovaných matematických výrazů
        self.render_theme_name = render_theme_name

    @classmethod
    async def attach_to_message(cls,
                                parent_message: discord.Message,
                                itx: discord.Interaction,
                                theme: str) -> None:
        """Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě ("úvodní obrazovce")"""
        self = cls(parent_message, itx.user, theme, itx.guild, render_get_theme(itx))
        self.add_item(self.subtheme_select)
        self.add_item(self.previous_button)
        self.add_item(self.next_button)
        if self.guild:
            self.add_item(self.save_button)
        self.add_item(ConfirmButton("Ukončit"))
        self.add_item(CustomExitButton())
        await parent_message.edit(content=f"# {self.theme_name}",
                                  view=self,
                                  embed=self.__generate_embed(""))

    async def interaction_check(self, itx: discord.Interaction) -> bool:
        # Tlačítko pro přeposlání podtématu do přímých zpráv může použít kdokoliv
        if itx.data["custom_id"] == "SubthemeSaveButton":
            return True
        # Ostatní View itemy určeny oprávněním daného serveru
        if permissions.view_interaction(itx, self.author, "explain_btns"):
            return True
        # Při nedostatečných právech informovat uživatele ephemeral zprávou
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False

    async def next_subtheme(self, itx: discord.Interaction) -> None:
        """Zobrazit následující podtéma aktuálně zvoleného tématu,
        nebo (pokud jsme na konci) ukončit a odeslat zprávu se selectem pro nové téma."""
        if self.subtheme_index < len(self.subtheme_names) - 1:
            self.subtheme_index += 1
            await self.__switch_subtheme(itx)
        else:
            await itx.response.send_message("Zvolte si téma:")
            await MessageView.attach_to_message(840,
                                                await itx.original_response(),
                                                itx.user,
                                                [TheoryThemeSelect()],
                                                "explain_btns")
            await delete_messages(itx, self.subtheme_messages)
            self.stop()

    async def previous_subtheme(self, itx: discord.Interaction) -> None:
        """Zobrazit předchozí podtéma aktuálně zvoleného tématu."""
        if self.subtheme_index > 0:
            self.subtheme_index -= 1
        await self.__switch_subtheme(itx)

    async def select_subtheme(self, itx: discord.Interaction, subtheme_name: str) -> None:
        """Zobrazit specifické podtéma aktuálně zvoleného tématu."""
        if subtheme_name in self.subtheme_names:
            self.subtheme_index = self.subtheme_names.index(subtheme_name)
        await self.__switch_subtheme(itx)

    def __get_subtheme_messages(self, render_theme_name: database.ThemeLiteral) -> list[Union[str, io.BytesIO]]:
        """
        :return:
            List textů/obrázků [str/io.BytesIO], které bude potřeba postupně odeslat pro vypsání aktuálního podtématu.
        """
        index = self.subtheme_index  # Index aktuálního podtématu
        header = self.subtheme_names[index]  # Název aktuálního podtématu
        # Text aktuálního podtématu
        body = self.subtheme_texts[index]
        result = raw_text_2_message_text(body, render_theme_name)
        # První odeslanou zprávou bude název podtématu (vložit ji na začátek listu)
        result.insert(0, f"## {header}")
        return result

    async def __switch_subtheme(self, itx: discord.Interaction) -> None:
        """Zobrazí podtéma odpovídající aktuální hodnotě self.subtheme_index a smaže zprávy předchozího podtématu."""
        index = self.subtheme_index
        header = self.subtheme_names[index]
        async with itx.channel.typing():
            # První odeslaná zpráva je reakce na interakci
            await itx.response.send_message(content=f"# {self.theme_name}", embed=self.__generate_embed(header))
            # Všechny odeslané zprávy si uložit, aby mohli být při další změně podtématu smazány
            new_messages = [await itx.original_response()]
            # Další zprávy už jsou normální zprávy do kanálu
            message_contents = self.__get_subtheme_messages(self.render_theme_name)
            new_messages.extend(await send_messages(itx, message_contents))
            # Enable/disable/... tlačítek
            self.previous_button.disabled = index == 0
            self.save_button.disabled = False  # True pouze při "úvodní obrazovce", na kterou se nelze vrátit
            if index == len(self.subtheme_names) - 1:
                self.next_button.label = "Změnit téma"
                self.next_button.emoji = "⤴️"
            else:
                self.next_button.label = "Další"
                self.next_button.emoji = "➡️"
            # Aktualizovat Select s podtématy (aktuální podtéma předvybráno)
            for option in self.subtheme_select.options:
                option.default = option.label == header
            # K poslední odeslané zprávě připnout sebe sama (view s tlačítky a selectem)
            self.parent_message = new_messages[-1]
            await self.parent_message.edit(view=self)
            # Staré zprávy smazat
            await delete_messages(itx, self.subtheme_messages)
            self.subtheme_messages = new_messages

    async def fwd_subtheme(self, itx: discord.Interaction) -> None:
        """Přeposlat aktuálně zobrazované podtéma uživateli do přímých zpráv."""
        if await try_dm_user(itx, f"# {self.theme_name}"):
            # Odeslat zprávy uživateli
            message_contents = self.__get_subtheme_messages(render_get_theme(itx, True))
            await send_messages(itx, message_contents, True)
            # Na interakci je třeba nějak zareagovat, jinak Discord hlásí, že se interakce nezdařila
            await itx.followup.send(content="Podtéma bylo přeposláno do DMs.", ephemeral=True)

    async def exit(self, itx: discord.Interaction) -> None:
        """Vše smazat a ukončit view."""
        await delete_messages(itx, self.subtheme_messages)
        self.stop()

    def __generate_embed(self, subtheme_name: str) -> discord.Embed:
        """Vygenerovat embed s přehledem podtémat, aktuálního podtématu a uživatele příkazu /explain."""
        embed_description = "".join(
            f"`>>` {x}\n" if subtheme_name == x else f"`  ` {x}\n" for x in self.subtheme_names
        )
        embed_message = discord.Embed(description=embed_description)
        embed_message.set_footer(text=f"{self.author.display_name} použil/a /explain", icon_url=self.author.avatar)
        return embed_message
# endregion
