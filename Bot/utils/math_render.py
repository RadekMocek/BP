import io
import re

import matplotlib.lines as lines
import matplotlib.pyplot as plt

__DPI = 180  # Rozlišení vykreslených obrázků
__COLOR_BACKGROUND = "#323337"  # Barva pozadí Discord chatu ve výchozím nastavení
__COLOR_FOREGROUND = "white"  # Barva písma pro tmavé pozadí
__MATRIX_CHAR_WIDTH = 0.011  # Šířka krátkého znaku v matici
__MATRIX_SPACE_WIDTH = 0.02  # Šířka mezery v matici
__MATRIX_SPACE_VERTICAL_MULTIPLIER = 2.2  # Výška mezery v matici = šířka * tato konstanta
__MATRIX_SPACE_HEIGHT = __MATRIX_SPACE_VERTICAL_MULTIPLIER * __MATRIX_SPACE_WIDTH
__MATRIX_BRACES_THICKNESS = 0.75  # Tloušťka závorek vykreslené matice

plt.rcParams["text.usetex"] = False  # Nepoužívat lokální TeX distribuci, ale Matplotlib renderer
plt.rcParams["text.parse_math"] = True
plt.rcParams["text.color"] = __COLOR_FOREGROUND
plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern


def render_tex(text_raw: str) -> io.BytesIO:
    """Vrací byte buffer obrázek s vykresleným TeX výrazem."""
    # O vykreslení matematického výrazu se stará Matplotlib
    fig = plt.figure()
    fig.patch.set_facecolor(__COLOR_BACKGROUND)
    __render_tex_at(fig, 0, 0, text_raw)
    # Obrázek není třeba ukládat lokálně, je uložen do byte bufferu a rovnou odeslán
    return __plt_to_image_buffer()


def render_matrix(text_raw: str) -> io.BytesIO:
    """Vrací byte buffer obrázek s vykreslenou maticí."""
    fig = plt.figure()
    fig.patch.set_facecolor(__COLOR_BACKGROUND)
    __render_matrix_at(fig, 0, 0, text_raw)
    return __plt_to_image_buffer()


def render_matrix_equation(text_raw: str) -> io.BytesIO:
    """Vrací byte buffer obrázek, kombinuje možnosti render_tex a render_matrix."""
    items_raw = re.split(r"([\[\]])", text_raw)  # Split podle hranatých závorek, závorky ponechat
    items = []  # Pole bude obsahovat finální TeX a matrix výrazy pro vykreslení
    index = 0
    previous = ""
    sqrt = False  # Odmocnina může mít syntax \sqrt[x]{y}, potřeba nebrat hranaté závorky jako závorky matice
    max_n_rows = 1  # Nejvyšší matice bude zabírat celou výšku obrázku, nižší výrazy budou zarovnány na střed
    items.append("")
    # Rozdělit na TeX a matrix výrazy:
    for item in items_raw:
        if item:
            if item == "[":
                if previous[-5:] == "\\sqrt":
                    sqrt = True
                else:
                    index += 1
                    items.append("")
            items[index] += item
            if item == "]":
                if sqrt:
                    sqrt = False
                else:
                    n_rows = items[index].count(";") + 1
                    if n_rows > max_n_rows:
                        max_n_rows = n_rows
                    index += 1
                    items.append("")
            previous = item
    # Vykreslit jednotlivé výrazy:
    fig = plt.figure()
    fig.patch.set_facecolor(__COLOR_BACKGROUND)
    x = 0
    text_y = max_n_rows / 2 * __MATRIX_SPACE_HEIGHT
    for item in items:
        if item:
            if item[0] == "[":
                n_rows = item.count(";") + 1
                matrix_y = (max_n_rows - n_rows) / 2 * __MATRIX_SPACE_HEIGHT
                matrix_width = __render_matrix_at(fig, x, matrix_y, item)
                x += matrix_width + __MATRIX_CHAR_WIDTH
            else:
                __render_tex_at(fig, x, text_y, item)
                x += __approx_tex_len(item) * __MATRIX_CHAR_WIDTH + __MATRIX_CHAR_WIDTH
    return __plt_to_image_buffer()


def __render_tex_at(fig, x: float, y: float, text_raw: str) -> None:
    # Obalit text do dolarů, pokud není
    if text_raw[0] == "$" and text_raw[-1] == "$":
        text_math = text_raw
    else:
        text_math = f"${text_raw}$"
    # Vykreslit text do fig
    fig.text(x=x, y=y, s=text_math, va="top")


def __render_matrix_at(fig, x: float, y: float, text: str) -> float:
    text = text.strip("[]")  # Zbavit se vnějších závorek, pokud jsou
    rows = text.split(";")  # Rozdělení na jednotlivé řádky matice
    items = []  # Pole bude obsahovat očesané prvky matice ve stylu [[a,b],[c,d]]
    max_item_len = 1  # Délka nejdelšího prvku matice
    max_n_cols = 1  # Počet sloupců matice

    # Naplnit items a zjistit správné hodnoty max_item_len a max_n_cols
    for row in reversed(rows):  # Řádky jsou prohozeny, protože plt má y=0 dole
        row_items = []
        cols = row.split(",")
        for col in cols:
            item = col.strip()  # Očesat od mezer
            if not item:
                item = "\\/"  # Pokud je prvek matice úplně prázdný, nahradit ho whitespace znakem
            row_items.append(item)

            item_len = __approx_tex_len(item)
            if item_len > max_item_len:
                max_item_len = item_len
        items.append(row_items)

        n_cols = len(cols)
        if n_cols > max_n_cols:
            max_n_cols = n_cols

    #
    max_item_len_with_space_scaled = max_item_len * __MATRIX_CHAR_WIDTH + __MATRIX_SPACE_WIDTH

    # Závorky matice – zjištění rohových bodů
    brace_space = (max_item_len * __MATRIX_CHAR_WIDTH / 2) + __MATRIX_CHAR_WIDTH
    x_left = x
    x_right = max_item_len_with_space_scaled * (max_n_cols - 1) + 2 * brace_space + x
    y_top = y + __MATRIX_SPACE_HEIGHT * len(rows)
    y_bot = y - __MATRIX_SPACE_WIDTH

    # Pokud je matice příliš úzká, přizpůsobit tvar závorek (zkrátit "nožky")
    braces_leg_size = __MATRIX_SPACE_WIDTH
    if max_n_cols == 1 and max_item_len < 5 or max_n_cols == 2 and max_item_len == 1:
        braces_leg_size /= 2

    # Levá a pravá závorka, každá tvořena čtyřmi body spojenými čárou
    fig.add_artist(lines.Line2D([x_left + braces_leg_size, x_left, x_left, x_left + braces_leg_size],
                                [y_bot, y_bot, y_top, y_top],
                                color=__COLOR_FOREGROUND,
                                lw=__MATRIX_BRACES_THICKNESS))
    fig.add_artist(lines.Line2D([x_right - braces_leg_size, x_right, x_right, x_right - braces_leg_size],
                                [y_bot, y_bot, y_top, y_top],
                                color=__COLOR_FOREGROUND,
                                lw=__MATRIX_BRACES_THICKNESS))

    # Vykreslení prvků matice
    row_n = 0
    for row in items:
        col_n = 0
        for item in row:
            fig.text(
                x=x + brace_space + max_item_len_with_space_scaled * col_n,
                y=y + __MATRIX_SPACE_HEIGHT * row_n,
                s=f"${item}$",
                ha="center",  # Horizontal alignment
            )
            col_n += 1
        row_n += 1

    return x_right - x


def __approx_tex_len(text: str) -> int:
    """Vrací PŘIBLIŽNOU (nadceněnou) délku TeX výrazu, jednotkou je počet krátkých znaků (Mathtext není monospace)."""
    # Vstupní řetězec je postupně upravován a nakonec je změřena jeho délka
    # 1 - Zlomky mají dva parametry (\frac{x}{y}), výraz \frac je zde zahozen, závorky jsou zahozeny později (krok 5)
    #   - V tuto chvíli může tedy zlomek být brán jako dvakrát širší, než je ve skutečnosti (\frac{123}{123} má délku 6)
    text = text.replace("\\frac", "")
    # 2 - Před každý symbol "\" je přidána mezera, aby správně fungoval výraz v dalším kroku
    text = text.replace("\\", " \\")
    # 3 - Hledáme výrazy začínající na "\", které jsou po libovolném počtu znaků ukončeny jedním ze znaků: " {_^()["
    #   - Ty jsou nahrazeny řetězcem "00", důležitá je délka řetězce len("00") == 2
    #   - Některé výrazy (např. \cdot) nejsou široké, jako dva krátké znaky, lepší ale délku nadcenit nežli podcenit
    text = re.sub(r"\\[^\s{_^()\[]*[\s{_^()\[]", "00", text + " ")
    # 4 - Znaky které jsou širší než běžná číslice jsou také nahrazeny dvouznakovým řetězcem "00"
    for ch in "+-=ABCDEFGHKMNOPQRUVWXYZmw":
        if ch in text:
            text = text.replace(ch, "00")
    # 5 - Znaky " _^{}[]" jsou zahozeny
    text = text.translate(str.maketrans("", "", " _^{}[]"))
    # 6 - Délka upraveného řetězce je vrácena
    return len(text)


def __plt_to_image_buffer() -> io.BytesIO:
    """Vrací byte buffer s uloženým obrázkem aktuální matplotlib.pyplot.figure."""
    buf = io.BytesIO()
    try:
        plt.savefig(fname=buf, dpi=__DPI, bbox_inches="tight", pad_inches=0.02, transparent=False)
    finally:
        plt.close()
    buf.seek(0)
    return buf
