import discord

from utils.theory_utils import list_themes, get_theme


class TheorySelect(discord.ui.Select):
    def __init__(self):
        options = []

        themes = list_themes()

        for theme in themes:
            options.append(discord.SelectOption(label=theme))

        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, itx: discord.Interaction):
        message_content = get_theme(self.values[0])
        await itx.response.send_message(content=message_content[:2000])
