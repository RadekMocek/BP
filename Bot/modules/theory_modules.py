"""Tlačítka, selecty, views užívaná při výkladu teorie."""

import io
import textwrap
from typing import Optional, Union

import discord

from modules.common_modules import ConfirmButton, CustomExitButton, LingeBotView
from modules.message_sender import send_messages
from utils.math_render import render_matrix_equation_align_to_buffer
from utils.theory_utils import get_theme, list_themes


# region Theory Buttons
class SubthemeNextButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="➡️", label="Další")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.next_subtheme(itx)


class SubthemePreviousButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="⬅️", label="Předchozí", disabled=True)

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.previous_subtheme(itx)


class SubthemeSaveButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="📨", label="Uložit do DMs", disabled=True, custom_id="SubthemeSaveButton")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.fwd_subtheme(itx)


# endregion

# region Theory Selects
class ThemeSelect(discord.ui.Select):
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
        await ThemeView.attach_to_message(await itx.original_response(),
                                          itx.user,
                                          chosen_theme,
                                          itx.guild)
        await itx.message.delete()


class SubthemeSelect(discord.ui.Select):
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
class ThemeView(LingeBotView):
    def __init__(self,
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User],
                 theme: str,
                 guild: Optional[discord.Guild]) -> None:
        super().__init__(parent_message=parent_message, author=author)
        self.guild = guild
        # Z utils.theory_utils získat název tématu a názvy+texty podtémat
        self.theme_name, self.subtheme_names, self.subtheme_texts = get_theme(theme)
        # Index právě zobrazovaného podtématu; začíná se na "úvodní obrazovce", proto -1 (mimo rozsah)
        self.subtheme_index = -1
        # Všechny zprávy použité pro vypsání  aktuálního podtématu uloženy v listu, aby mohli smazány, až bude třeba
        self.subtheme_messages: list[discord.Message] = [parent_message]
        # Na tato tlačítka si držet referenci, aby mohly být měněny jejich parametry (disabled) dle potřeby
        self.subtheme_select = SubthemeSelect(self.subtheme_names)
        self.previous_button = SubthemePreviousButton()
        self.next_button = SubthemeNextButton()
        self.save_button = SubthemeSaveButton()

    @classmethod
    async def attach_to_message(cls,
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User],
                                theme: str,
                                guild: Optional[discord.Guild]) -> None:
        # Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě ("úvodní obrazovce")
        self = cls(parent_message, author, theme, guild)
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
        # Ostatní View itemy může použít původní uživatel příkazu /explain nebo admin
        if itx.user == self.author or itx.user.guild_permissions.administrator:
            return True
        # Při nedostatečných právech informovat uživatele ephemeral zprávou
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False

    async def next_subtheme(self, itx: discord.Interaction) -> None:
        if self.subtheme_index < len(self.subtheme_names) - 1:
            self.subtheme_index += 1
        await self.__switch_subtheme(itx)

    async def previous_subtheme(self, itx: discord.Interaction) -> None:
        if self.subtheme_index > 0:
            self.subtheme_index -= 1
        await self.__switch_subtheme(itx)

    async def select_subtheme(self, itx: discord.Interaction, subtheme_name: str) -> None:
        if subtheme_name in self.subtheme_names:
            self.subtheme_index = self.subtheme_names.index(subtheme_name)
        await self.__switch_subtheme(itx)

    def __get_subtheme_messages(self) -> list[Union[str, io.BytesIO]]:
        """
        :return:
            List textů/obrázků [str/io.BytesIO], které bude potřeba postupně odeslat pro vypsání aktuálního podtématu.
        """
        index = self.subtheme_index  # Index aktuálního podtématu
        header = self.subtheme_names[index]  # Název aktuálního podtématu
        body = self.subtheme_texts[index]  # Text aktuálního podtématu
        body_parts = body.split("$$")  # Matematické výrazy očekáváme ve specifickém formátu: $$$render\nvýraz\n$$
        result: list[Union[str, io.BytesIO]] = [f"## {header}"]  # První odeslanou zprávou bude název podtématu
        for body_part in body_parts:
            if not body_part.isspace():  # Vynechat whitespace only
                if body_part[:7] == "$render":
                    # Při splnění formátu $$$render\nvýraz\n$$ vykreslit matematický výraz,
                    # případně přiložit chybu, byte buffer se uzavře až později při odesílání zpráv.
                    image_buffer = io.BytesIO()
                    try:
                        render_matrix_equation_align_to_buffer(image_buffer, body_part[7:].strip())
                        result.append(image_buffer)
                    except ValueError as error:
                        result.append(f"```{error}```")
                else:
                    # Limit pro délku zprávy na Discordu je 2000 znaků
                    if len(body_part) > 2000:
                        # Rozdělit na co nejdelší části tak, že maximální délka je 2000
                        # znaků, ale může se rozdělovat pouze podle whitespace znaků.
                        message_parts = textwrap.wrap(body_part,
                                                      width=2000,
                                                      expand_tabs=False,
                                                      replace_whitespace=False,
                                                      drop_whitespace=False,
                                                      break_long_words=False,
                                                      break_on_hyphens=False)
                        result.extend(message_parts)
                    else:
                        result.append(body_part)
        return result

    async def __switch_subtheme(self, itx: discord.Interaction) -> None:
        """Zobrazí podtéma odpovídající aktuální hodnotě self.subtheme_index a smaže zprávy předchozího podtématu."""
        index = self.subtheme_index
        header = self.subtheme_names[index]
        channel = itx.channel
        async with channel.typing():
            new_messages = []  # Všechny odeslané zprávy si uložit, aby mohli být při další změně podtématu smazány
            message_contents = self.__get_subtheme_messages()
            # První odeslaná zpráva je reakce na interakci
            await itx.response.send_message(content=f"# {self.theme_name}", embed=self.__generate_embed(header))
            new_messages.append(await itx.original_response())
            # Další zprávy už jsou normální zprávy do kanálu
            new_messages.extend(await send_messages(itx, message_contents))
            # Enable/disable tlačítek
            self.previous_button.disabled = index == 0
            self.next_button.disabled = index == len(self.subtheme_names) - 1
            self.save_button.disabled = False  # True pouze při "úvodní obrazovce", na kterou se nelze vrátit
            # Aktualizovat Select s podtématy (aktuální podtéma předvybráno)
            for option in self.subtheme_select.options:
                option.default = option.label == header
            # K poslední odeslané zprávě připnout sebe sama (view s tlačítky a selectem)
            self.parent_message = new_messages[-1]
            await self.parent_message.edit(view=self)
            # Staré zprávy smazat
            await self.delete_old_messages(itx)
            self.subtheme_messages = new_messages

    async def fwd_subtheme(self, itx: discord.Interaction) -> None:
        """Přeposlat aktuálně zobrazované podtéma uživateli do přímých zpráv."""
        await itx.response.defer()
        user = itx.user
        # Můžeme uživateli posílat přímé zprávy?
        try:
            await user.send(f"# {self.theme_name}")
        except discord.Forbidden:
            await itx.followup.send(
                content="Nemáte povolené přímé zprávy od členů tohoto serveru.\n"
                        "`Right click na ikonu serveru → Nastavení soukromí → Přímé zprávy`",
                ephemeral=True)
            return
        # Odeslat zprávy uživateli
        message_contents = self.__get_subtheme_messages()
        await send_messages(itx, message_contents, True)
        # Na interakci je třeba nějak zareagovat, jinak Discord hlásí, že se interakce nezdařila
        await itx.followup.send(content="Podtéma přeposláno do DMs.", ephemeral=True)

    async def delete_old_messages(self, itx: discord.Interaction):
        if not itx.response.is_done():
            await itx.response.defer()
        # if self.guild:
        #     await itx.channel.delete_messages(self.subtheme_messages)
        # else:  # 'DMChannel' object has no attribute 'delete_messages'
        # ???: channel.delete_messages() dělá problémy, občas nic nesmaže
        for old_message in self.subtheme_messages:
            try:
                await old_message.delete()
            except discord.errors.NotFound:
                pass  # Zpráva již byla smazána

    async def exit(self, itx: discord.Interaction) -> None:
        await self.delete_old_messages(itx)
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
