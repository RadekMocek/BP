"""Podpůrný modul pro práci s textovými řetězci."""

import io
import re
import textwrap
from typing import Union

import unicodeit

import utils.db_io as database
from utils.math_render import render_matrix_equation_align_to_buffer


def convert_html_tags(text: str) -> str:
    """Nahradit v řetězci tagy <sub/sup> za unicode znaky a <i> za podtržítka."""
    if not text:
        return text
    # <i>
    pattern = r"<\/?i>"
    text = re.sub(pattern, "_", text)
    # <sub> / <sup>
    pattern = r"<(sub|sup)>(.*?)</\1>"
    text = re.sub(pattern, __replace_sub_or_sup, text)
    return text


def __replace_sub_or_sup(match: re.Match[str]) -> str:
    tag_content = match.group(2)  # Řetězec mezi <tag> a </tag>
    is_sub = match.group(1) == "sub"  # Je tag <sub> nebo <sup>
    tex_char = "_" if is_sub else "^"
    replacement = unicodeit.replace(f"{tex_char}{{{tag_content}}}")
    # Pokud neexistuje unicode reprezentace pro všechny znaky v daném <sub></sub>, obalit vstupní text místo
    # toho do backquotes (single line codeblock, na Discordu se jedná o dobře vypadající alternativu za sub)
    if is_sub and "_" in replacement:
        replacement = f"`{tag_content}`"
    return replacement


def raw_text_2_message_text(text: str, render_theme_name: database.ThemeLiteral) -> list[Union[str, io.BytesIO]]:
    """Text z MD souboru rozdělit na textové a obrázkové části připravené pro odeslání na Discord."""
    result: list[Union[str, io.BytesIO]] = []
    text_parts = text.split("$$")  # Matematické výrazy očekáváme ve specifickém formátu: $$$render\nvýraz\n$$
    for text_part in text_parts:
        if not text_part.isspace():  # Vynechat whitespace only
            if text_part[:7] == "$render":
                # Při splnění formátu $$$render\nvýraz\n$$ vykreslit matematický výraz,
                # případně přiložit chybu, byte buffer se uzavře až později při odesílání zpráv.
                image_buffer = io.BytesIO()
                try:
                    render_matrix_equation_align_to_buffer(image_buffer, text_part[7:].strip(), render_theme_name)
                    result.append(image_buffer)
                except ValueError as error:
                    result.append(f"```{error}```")
            else:
                # Limit pro délku zprávy na Discordu je 2000 znaků
                if len(text_part) > 2000:
                    # Rozdělit na co nejdelší části tak, že maximální délka je 2000
                    # znaků, ale může se rozdělovat pouze podle whitespace znaků.
                    message_parts = textwrap.wrap(text_part,
                                                  width=2000,
                                                  expand_tabs=False,
                                                  replace_whitespace=False,
                                                  drop_whitespace=False,
                                                  break_long_words=False,
                                                  break_on_hyphens=False)
                    result.extend(message_parts)
                else:
                    result.append(text_part)
    return result
