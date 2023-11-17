import io

import discord
from discord import app_commands
from discord.ext import commands

from utils.math_render import render_matrix_equation_to_buffer


class Theory(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def explain(self, itx: discord.Interaction) -> None:
        """Testovací příkaz pro zobrazení vybrané látky z teorie."""
        await itx.response.defer()

        with open("static/02.MD", "r", encoding="utf-8") as file:
            message = file.read()

        message_parts = message.split("$$")
        channel = itx.channel

        for message_part in message_parts:
            if message_part[:7] == "$render":
                image_buffer = io.BytesIO()
                try:
                    render_matrix_equation_to_buffer(image_buffer, message_part[8:-1])
                    await channel.send(file=discord.File(image_buffer, "lingebot_math_render.png"))
                except ValueError as error:
                    await channel.send(f"```{error}```")
                finally:
                    image_buffer.close()
            else:
                await channel.send(message_part[:2000])

        await itx.followup.send("...")


async def setup(bot) -> None:
    await bot.add_cog(Theory(bot))
