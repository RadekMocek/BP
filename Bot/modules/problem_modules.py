"""Tlačítka, selecty, views užívaná při příkladech."""

import io
from datetime import datetime
from typing import Union

import discord

from modules.buttons import CustomExitButton
from modules.modals import LingeBotModal
from modules.views import LingeBotView
from utils.math_render import render_matrix_equation_align_to_buffer
from utils.problem_utils import ProblemManager


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


class AnswerCheckButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="🛂", label="Zkontrolovat výsledek")

    async def callback(self, itx: discord.Interaction) -> None:
        await itx.response.send_modal(self.view.modal)


class AnswerShowButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji="👁️", label="Zobrazit výsledek")

    async def callback(self, itx: discord.Interaction) -> None:
        await self.view.show(itx)


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
                 author: Union[discord.Member, discord.User]) -> None:
        super().__init__(parent_message=parent_message, author=author)
        self.problem_manager = ProblemManager()
        self.problem_select = ProblemSelect(self.problem_manager)
        self.generate_button = ProblemGenerateButton()
        self.check_button = AnswerCheckButton()
        self.show_button = AnswerShowButton()
        self.home_button = ProblemHomeButton()
        self.exit_button = CustomExitButton()
        self.modal = AnswerCheckModal(self)
        self.problem_name = ""
        self.is_any_problem_visible = False

    @classmethod
    async def attach_to_message(cls,
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User]) -> None:
        # Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě
        self = cls(parent_message, author)
        self.add_item(self.problem_select)
        self.add_item(self.generate_button)
        self.add_item(self.exit_button)
        await parent_message.edit(view=self)

    async def home(self, itx: discord.Interaction) -> None:
        self.is_any_problem_visible = False
        old_message = self.parent_message
        self.clear_items()
        self.add_item(self.problem_select)
        self.generate_button.disabled = True
        self.add_item(self.generate_button)
        self.add_item(self.exit_button)
        await itx.response.send_message(content="Zvolte si téma:", view=self)
        self.parent_message = await itx.original_response()
        await old_message.delete()

    async def select_problem(self, itx: discord.Interaction, problem_name: str) -> None:
        self.problem_name = problem_name
        old_message = self.parent_message
        # self.clear_items()
        self.generate_button.disabled = False
        embed_message = discord.Embed(title=problem_name)
        embed_message.set_footer(text=f"{self.author.display_name} použil/a /generate", icon_url=self.author.avatar)
        await itx.response.send_message(embed=embed_message, view=self)
        self.parent_message = await itx.original_response()
        await old_message.delete()

    async def generate(self, itx: discord.Interaction) -> None:
        old_message = self.parent_message
        task = self.problem_manager.generate_problem(self.problem_name)
        task_parts = task.split("$$$")
        # New message content
        content = task_parts[0]
        # New message image
        image_buffer = io.BytesIO()
        try:
            render_matrix_equation_align_to_buffer(image_buffer, task_parts[1])
        except ValueError as error:
            content += f"\n```{error}```"
        # New message embed
        embed_message = discord.Embed(timestamp=datetime.utcnow())
        embed_message.set_footer(text=f"{self.author.display_name} použil/a /generate", icon_url=self.author.avatar)
        # New message view items
        if not self.is_any_problem_visible:
            self.clear_items()
            self.generate_button.label = "Nový příklad"
            self.add_item(self.generate_button)
            self.add_item(self.check_button)
            self.add_item(self.show_button)
            self.add_item(self.home_button)
            self.is_any_problem_visible = True
        # Odeslat new message
        await itx.response.send_message(content=content,
                                        embed=embed_message,
                                        file=discord.File(image_buffer, "lingebot_math_render.png"),
                                        view=self)
        image_buffer.close()
        self.parent_message = await itx.original_response()
        await old_message.delete()

    async def exit(self, itx: discord.Interaction) -> None:
        try:
            await self.parent_message.delete()
        except discord.errors.NotFound:
            pass  # Zpráva již byla smazána
        self.stop()


# endregion

# region Problem Modals
class AnswerCheckModal(LingeBotModal):
    def __init__(self, view: ProblemView) -> None:
        super().__init__(title="Zadejte Váš výsledek")
        self.view = view
        self.add_item(discord.ui.TextInput(label="Výsledek",
                                           min_length=1,
                                           style=discord.TextStyle.paragraph))

    async def on_submit(self, itx: discord.Interaction) -> None:
        await itx.response.defer()
        text = self.children[0].value
        await itx.followup.send(content=f"Zadali jste výsledek `{text}`", ephemeral=True)
# endregion

# TODO: Embed – Čas je o hodinu posunutý
# TODO: Buttons – Práva
# TODO: Modal pro zkontrolování výsledku
# TODO: Zobrazit řešení
# TODO: Tutorial tlačítko pro příklady
