import discord

@discord.app_commands.command()
async def pow(self,
              itx: discord.Interaction,
              num: int,
              exp: int) -> None:
    """Umocní číslo 'num' na 'exp'."""
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Example",
                                    url="https://example.com"))
    await itx.response.send_message(content=num ** exp,
                                    view=view)