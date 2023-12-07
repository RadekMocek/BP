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
            message = await channel.send(message_content)
            sent_messages.append(message)
        elif isinstance(message_content, io.BytesIO):  # Obrázek s matematickým výrazem
            message = await channel.send(file=discord.File(message_content, "lingebot_math_render.png"))
            sent_messages.append(message)
            message_content.close()
    return sent_messages
