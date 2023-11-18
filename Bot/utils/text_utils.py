import re

import unicodeit


def sux_to_unicode(text: str) -> str:
    pattern = r"<(sub|sup)>(.*?)</\1>"
    result = re.sub(pattern, __replace_sux, text)
    return result


def __replace_sux(match):
    tag_content = match.group(2)  # Řetězec mezi <tag> a </tag>
    tag_name = match.group(1)  # Název tagu (sub/sup)
    tex_char = "^" if tag_name == "sup" else "_"
    replacement = unicodeit.replace(f"{tex_char}{{{tag_content}}}")
    return replacement
