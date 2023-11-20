import io
import textwrap
from typing import Union

import discord

from utils.math_render import render_matrix_equation_to_buffer
from utils.theory_utils import list_themes, get_theme


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


class ThemeExitButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="🚫", label="Ukončit")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.exit()


# endregion

# region Theory Selects
class ThemeSelect(discord.ui.Select):
    def __init__(self):
        options = []
        themes = list_themes()
        for theme in themes:
            options.append(discord.SelectOption(label=theme))
        super().__init__(placeholder="Zvolte si téma", min_values=1, max_values=1, options=options)

    async def callback(self, itx: discord.Interaction):
        self.view.stop()
        chosen_theme = self.values[0]
        await itx.response.send_message(content=f"Nahrávám {chosen_theme} ...")
        await ThemeView.attach_to_message(await itx.original_response(),
                                          itx.user,
                                          chosen_theme)
        await itx.message.delete()


class SubthemeSelect(discord.ui.Select):
    def __init__(self, subthemes: list[str]):
        options = []
        for subtheme in subthemes:
            options.append(discord.SelectOption(label=subtheme))
        super().__init__(placeholder="Zvolte si podtéma nebo využijte tlačítek",
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, itx: discord.Interaction):
        chosen_subtheme = self.values[0]
        await self.view.select_subtheme(itx, chosen_subtheme)
        # for option in self.options:
        #    option.default = option.label == chosen_subtheme


# endregion

# region Theory Views
class ThemeView(discord.ui.View):
    def __init__(self,
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User],
                 theme: str) -> None:
        super().__init__(timeout=None)  # Žádný timeout
        self.initial_parent_message = parent_message
        self.author = author
        self.theme_name, self.subtheme_names, self.subtheme_texts = get_theme(theme)
        self.subtheme_index = -1
        self.subtheme_messages: list[discord.Message] = [self.initial_parent_message]
        self.previous_button = SubthemePreviousButton()
        self.next_button = SubthemeNextButton()
        self.save_button = SubthemeSaveButton()

    @classmethod
    async def attach_to_message(cls,
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User],
                                theme: str) -> None:
        # Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě
        self = cls(parent_message, author, theme)
        self.add_item(SubthemeSelect(self.subtheme_names))
        self.add_item(self.previous_button)
        self.add_item(self.next_button)
        self.add_item(self.save_button)
        self.add_item(ThemeExitButton())
        await self.initial_parent_message.edit(content=f"# {self.theme_name}",
                                               view=self,
                                               embed=self.__generate_embed(""))

    async def interaction_check(self, itx: discord.Interaction) -> bool:
        # Tlačítko pro přeposlání podtématu do přímých zpráv může použít kdokoliv
        if itx.data["custom_id"] == "SubthemeSaveButton":
            return True
        # Ostatní View itemy může použít pouze autor původní zprávy nebo admin
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
        index = self.subtheme_index
        header = self.subtheme_names[index]
        body = self.subtheme_texts[index]
        body_parts = body.split("$$")
        result: list[Union[str, io.BytesIO]] = [f"## {header}"]
        for body_part in body_parts:
            if not body_part.isspace():
                if body_part[:7] == "$render":
                    image_buffer = io.BytesIO()
                    try:
                        render_matrix_equation_to_buffer(image_buffer, body_part[7:].strip())
                        result.append(image_buffer)
                    except ValueError as error:
                        result.append(f"```{error}```")
                else:
                    if len(body_part) > 2000:
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
        index = self.subtheme_index
        header = self.subtheme_names[index]
        channel = itx.channel
        async with channel.typing():
            new_messages = []
            message_contents = self.__get_subtheme_messages()

            await itx.response.send_message(content=f"# {self.theme_name}", embed=self.__generate_embed(header))
            new_messages.append(await itx.original_response())

            for message_content in message_contents:
                if isinstance(message_content, str):
                    message = await channel.send(message_content)
                    new_messages.append(message)
                elif isinstance(message_content, io.BytesIO):
                    message = await channel.send(file=discord.File(message_content, "lingebot_math_render.png"))
                    new_messages.append(message)
                    message_content.close()

            self.previous_button.disabled = index == 0
            self.next_button.disabled = index == len(self.subtheme_names) - 1
            self.save_button.disabled = False

            await new_messages[-1].edit(view=self)

            for old_message in self.subtheme_messages:
                try:
                    await old_message.delete()
                except discord.errors.NotFound:
                    pass  # Zpráva již byla smazána
            self.subtheme_messages = new_messages

    async def fwd_subtheme(self, itx: discord.Interaction) -> None:
        user = itx.user
        try:
            await user.send(f"# {self.theme_name}")
        except discord.Forbidden:
            await itx.response.send_message(
                content="Nemáte povolené přímé zprávy od členů tohoto serveru.\n"
                        "`Right click na ikonu serveru -> Nastavení soukromí -> Přímé zprávy`",
                ephemeral=True)
            return
        message_contents = self.__get_subtheme_messages()
        for message_content in message_contents:
            if isinstance(message_content, str):
                await user.send(message_content)
            elif isinstance(message_content, io.BytesIO):
                await user.send(file=discord.File(message_content, "lingebot_math_render.png"))
                message_content.close()
        await itx.response.send_message(content="Podtéma přeposláno do DMs.", ephemeral=True)

    async def exit(self) -> None:
        self.stop()
        for message in self.subtheme_messages:
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass  # Zpráva již byla smazána

    def __generate_embed(self, subtheme_name: str) -> discord.Embed:
        embed_description = "".join(
            f"`>>` {x}\n" if subtheme_name == x else f"`  ` {x}\n" for x in self.subtheme_names
        )
        embed_message = discord.Embed(description=embed_description)
        embed_message.set_footer(text=f"{self.author.display_name} použil/a /explain", icon_url=self.author.avatar)
        return embed_message
# endregion
