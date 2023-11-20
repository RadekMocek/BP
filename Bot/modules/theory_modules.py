import io
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
        self.add_item(ThemeExitButton())
        await self.initial_parent_message.edit(content=f"# {self.theme_name}",
                                               view=self,
                                               embed=self.__generate_embed(""))

    async def interaction_check(self, itx: discord.Interaction) -> bool:
        # View itemy může použít pouze autor původní zprávy nebo admin
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

    async def __switch_subtheme(self, itx: discord.Interaction) -> None:
        index = self.subtheme_index
        header = self.subtheme_names[index]
        body = self.subtheme_texts[index]

        body_parts = body.split("$$")
        channel = itx.channel

        async with channel.typing():
            new_messages = []

            await itx.response.send_message(content=f"# {self.theme_name}", embed=self.__generate_embed(header))
            new_messages.append(await itx.original_response())

            message = await channel.send(f"## {header}")
            new_messages.append(message)

            for body_part in body_parts:
                if not body_part.isspace():
                    if body_part[:7] == "$render":
                        image_buffer = io.BytesIO()
                        try:
                            render_matrix_equation_to_buffer(image_buffer, body_part[7:].strip())
                            message = await channel.send(file=discord.File(image_buffer, "lingebot_math_render.png"))
                            new_messages.append(message)
                        except ValueError as error:
                            message = await channel.send(f"```{error}```")
                            new_messages.append(message)
                        finally:
                            image_buffer.close()
                    else:
                        message = await channel.send(body_part[:2000])  # TODO
                        new_messages.append(message)

            self.previous_button.disabled = index == 0
            self.next_button.disabled = index == len(self.subtheme_names) - 1

            await new_messages[-1].edit(view=self)

            for old_message in self.subtheme_messages:
                try:
                    await old_message.delete()
                except discord.errors.NotFound:
                    pass  # Zpráva již byla smazána
            self.subtheme_messages = new_messages

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
