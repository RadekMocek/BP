import io
from typing import Union

import discord


async def send_messages(itx: discord.Interaction,
                        message_contents: list[Union[str, io.BytesIO]],
                        dm: bool = False) -> list[discord.Message]:
    channel = itx.user if dm else itx.channel
    sent_messages = []

    for message_content in message_contents:
        if isinstance(message_content, str):  # Text
            if message_content:  # If not empty
                message = await channel.send(message_content)
                sent_messages.append(message)
        elif isinstance(message_content, io.BytesIO):  # Obrázek s matematickým výrazem
            message = await channel.send(file=discord.File(message_content, "lingebot_math_render.png"))
            sent_messages.append(message)
            message_content.close()
    return sent_messages


async def delete_messages(itx: discord.Interaction, messages: list[discord.Message]):
    if not itx.response.is_done():
        await itx.response.defer()
    # if self.guild:
    #     await itx.channel.delete_messages(self.subtheme_messages)
    # else:  # 'DMChannel' object has no attribute 'delete_messages'
    # ???: channel.delete_messages() dělá problémy, občas nic nesmaže
    for old_message in messages:
        try:
            await old_message.delete()
        except discord.errors.NotFound:
            pass  # Zpráva již byla smazána


async def try_dm_user(itx: discord.Interaction, message: str) -> bool:
    if not itx.response.is_done():
        await itx.response.defer()
    # Můžeme uživateli posílat přímé zprávy?
    try:
        await itx.user.send(message)
    except discord.Forbidden:
        await itx.followup.send(
            content="Nemáte povolené přímé zprávy od členů tohoto serveru.\n"
                    "`Right click na ikonu serveru → Nastavení soukromí → Přímé zprávy`",
            ephemeral=True)
        return False
    return True
