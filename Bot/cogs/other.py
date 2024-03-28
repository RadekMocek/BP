"""Cog obstarávající ostatní nezařezené příkazy (/clear, /dm, /help, /ping)."""

import platform
from importlib.metadata import version

import discord
from discord import app_commands
from discord.ext import commands

import d_modules.permissions as permissions
from d_modules.bot import SECRET1
from d_modules.common_modules import MessageView, UrlGitBookButton, UrlGitHubButton, UrlGoogleFormsButton
from d_modules.messages import try_dm_user
from utils.file_io import txt_read


class Other(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def clear(self, itx: discord.Interaction) -> None:
        """Poslat dlouhou prázdnou zprávu (admin/DM only)."""
        permissions.check_command(itx, "clear")
        await itx.response.send_message("⠀\n" * 45)

    @app_commands.command()
    async def dm(self, itx: discord.Interaction) -> None:
        """Zahájit konverzaci v přímých zprávách."""
        is_ephemeral_but_may_fail = False
        if is_ephemeral_but_may_fail:
            if await try_dm_user(itx, "Zdravíčko!", False):
                await itx.response.send_message(content="Konverzace v DMs úspěšně zahájena.", ephemeral=True)
        else:
            if await try_dm_user(itx, "Zdravíčko!", True):
                await itx.followup.send(content="Konverzace v DMs úspěšně zahájena.")  # , ephemeral=True)
                # Ephemeral u followup zpráv v tomto případě nefunguje; omezení ze strany Discordu
                # https://github.com/discordjs/discord.js/issues/5702

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
        Kompletní nápověda se nachází na [GitBook](https://lingebot.gitbook.io/lingebot-napoveda/)*
        \* Na nové (lepší) verzi manuálu se pracuje
        
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
        # Základní informace
        description = (
            f"```Prodleva         {round(self.bot.latency * 1000)} ms```"
            f"```Uptime           {self.bot.get_uptime()}```"
            f"```Pčt. serverů     {len(self.bot.guilds)}```"
            f"```Hosting OS       {platform.system()} {platform.release()}```"
            f"```Python verze     {platform.python_version()}```"
        )
        # Informace o balíčcích
        packages = txt_read("requirements.txt")
        for line in packages.split("\n"):
            package_name = line.split("==")[0]
            description += f"` {package_name.ljust(20)}{version(package_name).ljust(7)}`\n"
        # Předa informace prostřednictvím embed zprávy
        embed_message = discord.Embed(title="Pong!", description=description)
        await itx.response.send_message(embed=embed_message, ephemeral=False)


async def setup(bot) -> None:
    await bot.add_cog(Other(bot))
