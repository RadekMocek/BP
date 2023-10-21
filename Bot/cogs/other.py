import discord
from discord import app_commands
from discord.ext import commands


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Ověřit dostupnost bota")
    async def ping(self, interaction: discord.Integration):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong!\nProdleva: {latency} ms")


async def setup(bot):
    await bot.add_cog(Other(bot))
