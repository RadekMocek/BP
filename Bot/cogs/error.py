import discord
from discord import app_commands
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        self.bot.tree.on_error = self.on_app_command_error

    @commands.Cog.listener()
    async def on_app_command_error(self, itx: discord.Interaction, error: app_commands.AppCommandError):
        await itx.followup.send(f"```{error}```")


async def setup(bot):
    await bot.add_cog(Error(bot))
