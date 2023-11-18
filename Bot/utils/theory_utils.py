import pathlib

from utils.text_utils import sux_to_unicode

static_files_path = pathlib.Path(__file__).parent.parent / "static"


def list_themes() -> list[str]:
    results = []
    static_dir = static_files_path
    for theme in static_dir.glob("*.MD"):
        results.append(theme.name)
    return results


def get_theme(filename: str) -> str:
    with open(static_files_path / filename, encoding="utf-8") as file:
        text = file.read()
    return sux_to_unicode(text)
