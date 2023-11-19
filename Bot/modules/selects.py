import discord

from modules.views import TheoryView
from utils.theory_utils import list_themes


class TheorySelect(discord.ui.Select):
    def __init__(self):
        options = []

        themes = list_themes()

        for theme in themes:
            options.append(discord.SelectOption(label=theme))

        super().__init__(placeholder="Zvolte si téma", max_values=1, min_values=1, options=options)

    async def callback(self, itx: discord.Interaction):
        self.view.stop()
        chosen_theme = self.values[0]
        await itx.response.send_message(content=f"Nahrávám {chosen_theme} ...")

        await TheoryView.attach_to_message(await itx.original_response(),
                                           itx.user,
                                           chosen_theme)

        await itx.message.delete()
