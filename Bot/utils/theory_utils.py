"""Podpůrný modul pro výklad teorie. Čte ze statických markdown souborů."""

import pathlib
import re

from utils.file_io import txt_read
from utils.text_utils import convert_html_tags

__THEORY_FILES_PATH = pathlib.Path(__file__).parent.parent / "_static" / "theory"
__files: dict[str, str] = {}


def list_themes() -> list[str]:
    """:return: List dostupných teoretických témat. Co téma, to markdown soubor."""
    global __files
    __files = {}
    for theme in __THEORY_FILES_PATH.glob("*.MD"):
        __files[theme.name[:-3]] = theme.name
    return list(__files.keys())


def get_theme(name: str) -> tuple[str, list[str], list[str]]:
    """Pro zvolené téma vrátí jeho název, názvy podtémat, texty podtémat (1:N:N)."""
    # Otevřít MD soubor s daným teoretickým tématem
    text = txt_read(__THEORY_FILES_PATH / __files[name])
    # Rozdělit podle nadpisů druhé úrovně (nadpisy podtémat)
    parts = re.split(r"(^##\s.*$)", text, flags=re.MULTILINE)
    # Soubor začíná nadpisem první úrovně (název tématu), hned po něm následuje první nadpis podtématu
    theme_name = parts[0].strip()[2:]  # Zahodit "# " před názvem a nové řádky po něm; máme název tématu
    parts.pop(0)  # Zahodit název tématu kvůli dalšímu kroku
    # Podtémata – nadpisy a k nim příslušný text
    subtheme_names = [x[3:] for x in parts[0::2]]  # Zahodit "## "
    subtheme_texts = [convert_html_tags(x) for x in parts[1::2]]  # U textu převést html tagy jako <sub> apod.
    # Vrátit název tématu, názvy podtémat, texty podtémat
    return theme_name, subtheme_names, subtheme_texts
