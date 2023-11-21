"""Podpůrný modul pro práci s textovými řetězci."""

import re

import unicodeit


def convert_html_tags(text: str) -> str:
    # <i>
    pattern = r"<\/?i>"
    text = re.sub(pattern, "_", text)
    # <sub> / <sup>
    pattern = r"<(sub|sup)>(.*?)</\1>"
    text = re.sub(pattern, __replace_sub_or_sup, text)
    return text


def __replace_sub_or_sup(match: re.Match[str]) -> str:
    tag_content = match.group(2)  # Řetězec mezi <tag> a </tag>
    tag_name = match.group(1)  # Název tagu (sub/sup)
    tex_char = "^" if tag_name == "sup" else "_"
    replacement = unicodeit.replace(f"{tex_char}{{{tag_content}}}")
    return replacement
