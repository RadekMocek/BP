"""Tlačítka, selecty, views užívaná při příkladech."""

from typing import Union

import discord

from modules.views import LingeBotView
from utils.problem_utils import ProblemManager


# region Problem Buttons
# endregion

# region Problem Selects
class ProblemSelect(discord.ui.Select):
    def __init__(self, problem_manager: ProblemManager) -> None:
        options = []
        problems = problem_manager.list_problems()
        for problem in problems:
            options.append(discord.SelectOption(label=problem))
        super().__init__(placeholder="Zvolte si téma", min_values=1, max_values=1, options=options)


# endregion

# region Problem Views
class ProblemView(LingeBotView):
    def __init__(self,
                 parent_message: discord.Message,
                 author: Union[discord.Member, discord.User]) -> None:
        super().__init__(parent_message=parent_message, author=author)
        self.problem_manager = ProblemManager()

    @classmethod
    async def attach_to_message(cls,
                                parent_message: discord.Message,
                                author: Union[discord.Member, discord.User]) -> None:
        # Vytvořit instanci sebe sama, přidat do ní dané itemy a přiřadit ji k dané zprávě
        self = cls(parent_message, author)
        self.add_item(ProblemSelect(self.problem_manager))
        await parent_message.edit(view=self)
# endregion
