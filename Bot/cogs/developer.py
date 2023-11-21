"""Cog obstarávající příkazy pro údržbu vývojářem."""

from discord.ext import commands


class Developer(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def slash_sync(self, ctx: commands.Context) -> None:
        synchronized = await ctx.bot.tree.sync()
        await ctx.send(f"Synchronizované příkazy:\n```/" + "\n/".join([x.name for x in synchronized]) + "```")


async def setup(bot) -> None:
    await bot.add_cog(Developer(bot))
