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
    is_sub = match.group(1) == "sub"  # Je tag <sub> nebo <sup>
    tex_char = "_" if is_sub else "^"
    replacement = unicodeit.replace(f"{tex_char}{{{tag_content}}}")

    if is_sub and "_" in replacement:
        replacement = f"`{tag_content}`"

    return replacement
