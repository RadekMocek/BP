"""Podpůrný modul pro výklad teorie. Momentálně čte ze statických markdown souborů."""

import pathlib
import re
from typing import Tuple

from utils.text_utils import convert_html_tags

static_files_path = pathlib.Path(__file__).parent.parent / "static"


def list_themes() -> list[str]:
    results = []
    static_dir = static_files_path
    for theme in static_dir.glob("*.MD"):
        results.append(theme.name)
    return results


def get_theme(filename: str) -> Tuple[str, list[str], list[str]]:
    with open(static_files_path / filename, encoding="utf-8") as file:
        text = file.read()

    pattern = r"(^##\s.*$)"
    result = re.split(pattern, text, flags=re.MULTILINE)

    theme_name = result[0].strip()[2:]
    result.pop(0)
    subtheme_names = [x[3:] for x in result[0::2]]
    subtheme_texts = [convert_html_tags(x) for x in result[1::2]]

    return theme_name, subtheme_names, subtheme_texts