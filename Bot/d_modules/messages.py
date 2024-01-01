"""Modul pro práci se zprávami."""

import asyncio
import io
from typing import Union

import discord

__DELAY_DURATION = 0.15


async def send_messages(itx: discord.Interaction,
                        message_contents: list[Union[str, io.BytesIO]],
                        dm: bool = False) -> list[discord.Message]:
    """Odeslat zprávy do určitého kanálu nebo určitému uživateli."""
    channel = itx.user if dm else itx.channel
    sent_messages = []
    # Při větším množství zpráv snížit rychlost jejich odesílání kvůli Discord omezením
    delay = len(message_contents) > 5

    for message_content in message_contents:
        if isinstance(message_content, str):  # Text
            if message_content:  # If not empty
                message = await channel.send(message_content)
                sent_messages.append(message)
        elif isinstance(message_content, io.BytesIO):  # Obrázek s matematickým výrazem
            message = await channel.send(file=discord.File(message_content, "lingebot_math_render.png"))
            sent_messages.append(message)
            message_content.close()
        if delay:
            await asyncio.sleep(__DELAY_DURATION)
    return sent_messages


async def delete_messages(itx: discord.Interaction, messages: list[discord.Message]):
    """Smazat zprávy."""
    if not itx.response.is_done():
        await itx.response.defer()

    # ???: channel.delete_messages() dělá problémy a občas nic nesmaže
    # ???: klasické mazání po jednom zavolané po něm pak taky nefunguje
    # if itx.guild:  # 'DMChannel' object has no attribute 'delete_messages'
    #     await itx.channel.delete_messages(messages)

    # V přímých zprávách je nutné zprávy mazat po jednom, (na serveru taky kvůli problémům s channel.delete_messages())
    delay = len(messages) > 5
    for old_message in messages:
        try:
            await old_message.delete()
            if delay:
                await asyncio.sleep(__DELAY_DURATION)
        except discord.errors.NotFound:
            pass  # Zpráva již byla smazána


async def try_dm_user(itx: discord.Interaction, message: str) -> bool:
    """Zkusit uživateli odeslat přímou zprávu. Pokud má uživatel zakázané přímé zprávy od
    členů serveru, informovat jej o tom ephemeral zprávou v kanále, kde vznikla interakce."""
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
