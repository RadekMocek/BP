"""Cog obstarávající ostatní nezařezené příkazy."""

import platform
from importlib.metadata import version

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
from d_modules.bot import LingeBot, SECRET1
from d_modules.common_modules import MessageView, UrlGitBookButton, UrlGitHubButton, UrlGoogleFormsButton
from d_modules.messages import try_dm_user


class Other(commands.Cog):
    def __init__(self, bot: LingeBot) -> None:
        self.bot: LingeBot = bot

    @app_commands.command()
    async def clear(self, itx: discord.Interaction) -> None:
        """Poslat dlouhou prázdnou zprávu (admin/DM only)."""
        permissions.command(itx, "clear")
        await itx.response.send_message("⠀\n" * 45)

    @app_commands.command()
    async def dm(self, itx: discord.Interaction) -> None:
        """Zahájit konverzaci v přímých zprávách."""
        if await try_dm_user(itx, "Zdravíčko!", False):
            await itx.response.send_message(content="Konverzace v DMs úspěšně zahájena.", ephemeral=True)

    @app_commands.command()
    async def help(self, itx: discord.Interaction) -> None:
        """Zobrazit nápovědu."""
        embed_message = discord.Embed(title="Nápověda", description=f"""
        LingeBot je bot zaměřený na výklad a příklady z lineární algebry a vznikl jako součást BP na FM TUL
        
        ### Dostupné příkazy
        `/explain ` – Otevřít rozhraní pro výklad teorie
        `/generate` – Otevřít rozhraní pro příklady
        `/render  ` – Vykreslit matematický výraz
        
        `/clear` – Pročistit chat (poslat dlouhou prázdnou zprávu)
        `/dm   ` – Zahájit konverzaci v přímých zprávách
        `/help ` – Zobrazit tuto nápovědu
        `/ping ` – Ověřit dostupnost bota
        
        `/setup` – Nastavení pro administrátory (viz podrobná nápověda)
        
        ### Podrobná nápověda
        Kompletní nápověda se nachází na [GitBook](https://lingebot.gitbook.io/lingebot-napoveda/)
        
        ### Zpětná vazba
        Jedním z bodů mé práce je také __**vyhodnotit zpětnou vazbu od uživatelů**__
        
        Pokud budete bota používat, vyplňte pak prosím tento dotazník:
        {SECRET1}        
        
        Děkuji
        """)
        await itx.response.send_message(embed=embed_message)
        await MessageView.attach_to_message(None,
                                            await itx.original_response(),
                                            itx.user,
                                            [UrlGitBookButton(), UrlGitHubButton(), UrlGoogleFormsButton()])

    @app_commands.command()
    async def ping(self, itx: discord.Interaction) -> None:
        """Ověřit dostupnost bota."""
        ljust_amount = 7
        rjust_amount = 17
        embed_message = discord.Embed(title="Pong!", description=(
            f"```Prodleva         {round(self.bot.latency * 1000)} ms```"
            f"```Uptime           {self.bot.get_uptime()}```"
            f"```Pčt. serverů     {len(self.bot.guilds)}```"
            f"```Hosting OS       {platform.system()} {platform.release()}```"
            f"```Python verze     {platform.python_version()}```"
            f"` discord.py{version('discord.py').ljust(ljust_amount).rjust(rjust_amount)}`\n"
            f"` matplotlib{version('matplotlib').ljust(ljust_amount).rjust(rjust_amount)}`\n"
            f"` numpy     {version('numpy').ljust(ljust_amount).rjust(rjust_amount)}`\n"
            f"` sympy     {version('sympy').ljust(ljust_amount).rjust(rjust_amount)}`\n"
            f"` unicodeit {version('unicodeit').ljust(ljust_amount).rjust(rjust_amount)}`"
        ))
        await itx.response.send_message(embed=embed_message, ephemeral=False)


async def setup(bot) -> None:
    await bot.add_cog(Other(bot))
