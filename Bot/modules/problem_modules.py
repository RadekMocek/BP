"""Tlačítka, selecty, views užívaná při příkladech."""

import io
from datetime import datetime
from typing import Optional, Union

import discord

from modules.common_modules import CustomExitButton, LingeBotView, MessageView
from modules.messages import delete_messages, send_messages, try_dm_user
from utils.math_render import render_matrix_equation_align_to_buffer
from utils.problem_utils import ProblemManager, get_problem_tutorial
from utils.text_utils import raw_text_2_message_text


# region Problem Buttons
class ProblemHomeButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="⤴️", label="Změnit téma / Ukončit")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.home(itx)


class ProblemGenerateButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="🧮", label="Generovat příklad", disabled=True)

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.generate(itx)


class ProblemTutorialButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="❔", label="Jak počítat?", disabled=True)

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.tutorial(itx)


class ProblemAnswerShowButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="🛂", label="Zobrazit výsledek")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.show_answer(itx)


class TutorialSaveButton(discord.ui.Button):
    def __init__(self, problem_name: str, tutorial_text: str) -> None:
        super().__init__(emoji="📨", label="Uložit do DMs")
        self.tutorial_text = tutorial_text
        self.problem_name = problem_name

    async def callback(self, itx: discord.Interaction) -> None:
        if await try_dm_user(itx, f"Jak počítat _{self.problem_name}_?"):
            await send_messages(itx, raw_text_2_message_text(self.tutorial_text), True)
            await itx.followup.send(content="Podtéma přeposláno do DMs.", ephemeral=True)


# endregion

# region Problem Selects
class ProblemSelect(discord.ui.Select):
    def __init__(self, problem_manager: ProblemManager) -> None:
        options = []
        problems = problem_manager.list_problems()
        for problem in problems:
            options.append(discord.SelectOption(label=problem))
        super().__init__(placeholder="Zvolte si téma", min_values=1, max_values=1, options=options)

    async def callback(self, itx: discord.Interaction) -> None:
        chosen_problem = self.values[0]
        await self.view.select_problem(itx, chosen_problem)


# endregion

# region Problem Views
class ProblemView(LingeBotView):
    def __init__(self,
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User],
                 guild: Optional[discord.Guild]) -> None:
        super().__init__(parent_message=parent_message, author=author)
        self.guild = guild
        self.problem_manager = ProblemManager()
        self.problem_select = ProblemSelect(self.problem_manager)
        self.generate_button = ProblemGenerateButton()
        self.tutorial_button = ProblemTutorialButton()
        self.show_button = ProblemAnswerShowButton()
        self.home_button = ProblemHomeButton()
        self.exit_button = CustomExitButton()
        self.problem_name = ""
        self.is_any_problem_visible = False
        self.answer = ""
        self.tutorial_text = ""
        self.tutorial_messages: list[discord.Message] = []

    @classmethod
    async def attach_to_message(cls,
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User],
                                guild: Optional[discord.Guild]) -> None:
        # Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě
        self = cls(parent_message, author, guild)
        self.add_item(self.problem_select)
        self.add_item(self.generate_button)
        self.add_item(self.tutorial_button)
        self.add_item(self.exit_button)
        await parent_message.edit(view=self)

    async def interaction_check(self, itx: discord.Interaction) -> bool:
        # View může použít původní uživatel příkazu /generate nebo admin
        if itx.user == self.author or itx.user.guild_permissions.administrator:
            return True
        # Při nedostatečných právech informovat uživatele ephemeral zprávou
        message_content = "Nemáte dostatečná práva pro interakci s touto zprávou."
        await itx.response.send_message(content=message_content, ephemeral=True)
        return False

    async def home(self, itx: discord.Interaction) -> None:
        self.is_any_problem_visible = False
        self.clear_items()
        self.add_item(self.problem_select)
        for option in self.problem_select.options:
            option.default = False
        self.generate_button.disabled = True
        self.add_item(self.generate_button)
        self.tutorial_button.disabled = True
        self.add_item(self.tutorial_button)
        self.add_item(self.exit_button)
        await itx.response.edit_message(content="Zvolte si téma:", embed=None, attachments=[], view=self)

    async def select_problem(self, itx: discord.Interaction, problem_name: str) -> None:
        self.problem_name = problem_name

        tutorial_text = get_problem_tutorial(self.problem_name)
        if tutorial_text:
            self.tutorial_text = tutorial_text
            self.tutorial_button.disabled = False

        # Aktualizovat Select s tématy (aktuální téma předvybráno)
        for option in self.problem_select.options:
            option.default = option.label == problem_name

        self.generate_button.disabled = False
        await itx.response.edit_message(embed=self.__generate_embed(True), view=self)

    async def generate(self, itx: discord.Interaction) -> None:
        # New message view items
        if not self.is_any_problem_visible:
            self.clear_items()
            self.generate_button.label = "Nový příklad"
            self.generate_button.emoji = "🆕"
            self.add_item(self.generate_button)
            self.add_item(self.show_button)
            self.add_item(self.home_button)
            self.is_any_problem_visible = True
        self.show_button.disabled = False
        # "Odeslat" new message a nastavit answer
        task, self.answer = self.problem_manager.generate_problem(self.problem_name)
        await self.__edit_message(itx, task)

    async def show_answer(self, itx: discord.Interaction) -> None:
        self.show_button.disabled = True
        await self.__edit_message(itx, self.answer)

    async def __edit_message(self, itx: discord.Interaction, text: str):
        # Content
        text_parts = text.split("$$$")
        content = text_parts[0]
        # Image
        image_buffer = io.BytesIO()
        try:
            render_matrix_equation_align_to_buffer(image_buffer, text_parts[1])
        except ValueError as error:
            content += f"\n```{error}```"
        # Upravit parent_message
        await itx.response.edit_message(content=content,
                                        embed=self.__generate_embed(False),
                                        attachments=[discord.File(image_buffer, "lingebot_math_render.png")],
                                        view=self)
        image_buffer.close()

    async def tutorial(self, itx: discord.Interaction) -> None:
        await itx.response.defer()
        async with itx.channel.typing():
            new_tutorial_messages = await send_messages(itx, raw_text_2_message_text(self.tutorial_text))
            new_parent_message = await itx.followup.send(embed=self.__generate_embed(True), view=self)

            if self.guild:
                await MessageView.attach_to_message(840,
                                                    new_tutorial_messages[-1],
                                                    itx.user,
                                                    [TutorialSaveButton(self.problem_name, self.tutorial_text)],
                                                    True)

            self.tutorial_messages.append(self.parent_message)
            await delete_messages(itx, self.tutorial_messages)

            self.tutorial_messages = new_tutorial_messages
            self.parent_message = new_parent_message

    async def exit(self, itx: discord.Interaction) -> None:
        self.tutorial_messages.append(self.parent_message)
        await delete_messages(itx, self.tutorial_messages)
        self.stop()

    def __generate_embed(self, title: bool) -> discord.Embed:
        embed_message = discord.Embed(title=self.problem_name) if title else discord.Embed(timestamp=datetime.now())
        embed_message.set_footer(text=f"{self.author.display_name} použil/a /generate", icon_url=self.author.avatar)
        return embed_message

# endregion
