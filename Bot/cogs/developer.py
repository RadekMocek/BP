"""Cog obstarávající příkazy pro údržbu vývojářem."""
import discord
from discord.ext import commands

import utils.db_io as database
from d_modules.common_modules import MessageView, UrlGoogleFormsButton


class Developer(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def slash_sync(self, ctx: commands.Context) -> None:
        """Globálně synchronizovat slash commands."""
        synchronized = await ctx.bot.tree.sync()
        await ctx.send(f"Synchronizované příkazy:\n```/" + "\n/".join([x.name for x in synchronized]) + "```")

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def purge_table(self, ctx: commands.Context, *, table_name: str) -> None:
        """Smazat všechny hodnoty z určité tabulky v databázi."""
        database.purge_table(table_name)
        await ctx.send(f"Tabulka `{table_name}` vyčištěna.")

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def questionnaire_construction(self, ctx: commands.Context, *, text: str) -> None:
        """Oznámení dotazníkového šetření."""
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    message = await channel.send(text, embeds=[])
                    await MessageView.attach_to_message(None, message, ctx.author, [UrlGoogleFormsButton()])
                    print(f"Dotazník byl odeslán do [{guild} :: {channel}]")
                    break
                except discord.errors.HTTPException:
                    pass


async def setup(bot) -> None:
    await bot.add_cog(Developer(bot))
