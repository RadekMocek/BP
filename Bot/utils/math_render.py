"""Podpůrný modul pro vykreslování matematických výrazů."""

import io
import re

import matplotlib.lines as lines
import matplotlib.pyplot as plt

import utils.db_io as database

__DPI = 180  # Rozlišení vykreslených obrázků
__CHAR_WIDTH = 0.011  # Šířka krátkého znaku
__CHAR_HEIGHT = 0.05  # Výška znaku i s mezerou
__SPACE_WIDTH = 0.02  # Šířka mezery mezi částmi výrazu / prvky v matici
__ALIGN_SPACE_HEIGHT_ADDITION = 0.03  # Dodatečná mezera mezi řádky víceřádkového výrazu
__MATRIX_BRACES_THICKNESS = 0.75  # Tloušťka závorek vykreslené matice

plt.rcParams["text.usetex"] = False  # Nepoužívat lokální TeX distribuci, ale Matplotlib renderer
plt.rcParams["text.parse_math"] = True
plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern


def __get_theme_colors(render_theme_name: database.ThemeLiteral) -> tuple[str, str]:
    match render_theme_name:
        case "light":
            return "#ffffff", "black"
        case "midnight":
            return "#000000", "white"
        case "solar":
            return "#fdf6e3", "black"
        case _:  # "dark"
            return "#323337", "white"


def render_matrix_equation_align_to_buffer(buffer: io.BytesIO,
                                           text_raw: str,
                                           render_theme_name: database.ThemeLiteral) -> None:
    """Do byte bufferu vloží obrázek s vykresleným matematickým ~TeX výrazem, používá
    Matplotlib Mathtext a přidává možnost vykreslovat matice, jejichž syntax je podobný
    maticím v MATLABu. Umí vykreslit víceřádkové výrazy (\\\\) a zarovnat je podle ampersandu."""
    color_background, color_foreground = __get_theme_colors(render_theme_name)
    plt.rcParams["text.color"] = color_foreground
    plt.rcParams["lines.color"] = color_foreground
    fig = plt.figure()
    fig.patch.set_facecolor(color_background)
    __render_matrix_equation_align_to_buffer(fig, text_raw)
    __plt_to_image_buffer(buffer)


def __render_matrix_equation_align_to_buffer(fig: plt.figure, text_raw: str) -> None:
    if "\\\\" in text_raw:  # Víceřádkový výraz:
        align_lines = text_raw.split("\\\\")
        align_y = 0  # Souřadnice y aktuálně vykreslovaného řádku
        for line_raw in align_lines:  # Pro každý řádek výrazu:
            line = line_raw.strip()
            ampersand_index = line.find("&")
            any_matrices = line.count("[") > line.count("\\sqrt[")
            if ampersand_index != -1:
                # Pokud text obsahuje "&", zahodit tento znak a vykreslit tak, aby se byl nacházel na souřadnici x=0
                text_left = line[:ampersand_index]
                text_right = line[ampersand_index + 1:]
                # Pokud tento řádek obsahuje matice, nelze použít horizontal align (ha).
                # Využije se tedy přibližná délka levé strany řádku:
                if any_matrices:
                    line_height = __render_matrix_equation_at(fig,
                                                              text_left + text_right,
                                                              -__approx_tex_len(text_left) * __CHAR_WIDTH,
                                                              align_y,
                                                              True)
                # Jinak využít ha:
                else:
                    line_height = __render_matrix_equation_at(fig, text_left, 0, align_y, False, "right")
                    __render_matrix_equation_at(fig, text_right, 0, align_y, False)
            else:
                line_height = __render_matrix_equation_at(fig, line, 0, align_y, any_matrices)
            align_y -= line_height
    else:  # Jednořádkový výraz:
        any_matrices = text_raw.count("[") > text_raw.count("\\sqrt[")
        __render_matrix_equation_at(fig, text_raw, 0, 0, any_matrices)


def __render_matrix_equation_at(fig: plt.figure,
                                text_raw: str,
                                start_x: float,
                                start_y: float,
                                any_matrices: bool,
                                ha: str = "left") -> float:
    """
    Vykreslit matematický výraz s maticemi `text_raw` do `fig` na souřadnice `start_x`, `start_y`.

    :return: Výška vykresleného výrazu.
    """
    if not any_matrices and text_raw:
        __render_tex_at(fig, start_x, start_y, text_raw, ha)
        return __CHAR_HEIGHT + __ALIGN_SPACE_HEIGHT_ADDITION

    items_raw = re.split(r"([\[\]])", text_raw)  # Split podle hranatých závorek, závorky ponechat
    items = []  # Pole bude obsahovat finální TeX a matrix výrazy pro vykreslení
    index = 0
    previous = ""
    sqrt = False  # Odmocnina může mít syntax \sqrt[x]{y}, potřeba nebrat hranaté závorky jako závorky matice
    max_n_rows = 1  # Nejvyšší matice bude zabírat celou výšku obrázku, nižší výrazy budou zarovnány na střed
    items.append("")
    # Rozdělit na TeX a matrix výrazy:
    for item in items_raw:
        if item:  # Vynechat prázdné
            if item == "[":  # Začátek matice / argumentu odmocniny
                if previous[-5:] == "\\sqrt":  # Začátek argumentu odmocniny
                    sqrt = True
                else:  # Začátek matice – začít vkládat do nové pozice v items
                    index += 1
                    items.append("")
            items[index] += item  # Vložit tex/matrix výraz na aktuální pozici v items
            if item == "]":  # Konec matice / argumentu odmocniny
                if sqrt:  # Pokud byl otevřen argument odmocniny, jedná se o jeho ukončení
                    sqrt = False
                else:  # Jinak je to konec matice
                    # Kontrola výšky matice, zdali není nové maximum
                    n_rows = items[index].count(";") + 1
                    if n_rows > max_n_rows:
                        max_n_rows = n_rows
                    # Začít vkládat do nové pozice v items
                    index += 1
                    items.append("")
            previous = item  # Pamatovat si předchozí položku kvůli detekci odmocnin
    # Vykreslit jednotlivé výrazy:
    x = start_x
    text_y = start_y - max_n_rows / 2 * __CHAR_HEIGHT + __SPACE_WIDTH / 2
    last_item_index = len(items) - 1
    for index, item in enumerate(items):
        if item:
            if item[0] == "[":  # Matrix
                n_rows = item.count(";") + 1
                matrix_y = start_y - ((max_n_rows - n_rows) / 2 * __CHAR_HEIGHT)
                matrix_width = __render_matrix_at(fig, x, matrix_y, item)
                x += matrix_width + __CHAR_WIDTH
            else:  # TeX
                __render_tex_at(fig, x, text_y, item, ha)
                if index != last_item_index:  # U poslední části výrazu není třeba počítat její šířku
                    x += __approx_tex_len(item) * __CHAR_WIDTH + __CHAR_WIDTH
    return max_n_rows * __CHAR_HEIGHT + __ALIGN_SPACE_HEIGHT_ADDITION


def __render_tex_at(fig: plt.figure, x: float, y: float, text_raw: str, ha: str = "left") -> None:
    """Vykreslit matematický výraz `text_raw` do `fig` na souřadnice `x`, `y`."""
    # Obalit text do dolarů, pokud není
    if text_raw[0] == "$" and text_raw[-1] == "$":
        text_math = text_raw
    else:
        text_math = f"${text_raw}$"
    # Vykreslit text do `fig`
    fig.text(x=x, y=y, s=text_math, ha=ha)


def __render_matrix_at(fig: plt.figure, x: float, y: float, text: str) -> float:
    """
    Vykreslit matici popsanou v `text` do `fig` na souřadnice `x`, `y`.

    :return: Šířka vykreslené matice.
    """
    text = text.strip("[]")  # Zbavit se vnějších závorek, pokud jsou
    rows = text.split(";")  # Rozdělení na jednotlivé řádky matice
    items = []  # Pole bude obsahovat očesané prvky matice ve stylu [[a,b],[c,d]]
    max_item_len = 1  # Délka nejdelšího prvku matice
    max_n_cols = 1  # Počet sloupců matice

    # Matice bude vykreslována odspodu, `y` ale značí vrchol matice, proto je posunut
    n_rows = len(rows)
    y -= __CHAR_HEIGHT * (n_rows - 1) + __SPACE_WIDTH

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

    # Šířka sloupce s mezerou
    max_item_len_with_space_scaled = max_item_len * __CHAR_WIDTH + __SPACE_WIDTH

    # Závorky matice – zjištění rohových bodů
    brace_space = (max_item_len * __CHAR_WIDTH / 2) + __CHAR_WIDTH
    # x_left = x
    x_right = x + max_item_len_with_space_scaled * (max_n_cols - 1) + 2 * brace_space
    y_top = y + __CHAR_HEIGHT * n_rows
    y_bot = y - __SPACE_WIDTH

    # Pokud je matice příliš úzká, přizpůsobit tvar závorek (zkrátit "nožky")
    braces_leg_size = __SPACE_WIDTH
    if max_n_cols == 1 and max_item_len < 5 or max_n_cols == 2 and max_item_len == 1:
        braces_leg_size /= 2

    # Levá a pravá závorka, každá tvořena čtyřmi body spojenými čárou
    fig.add_artist(lines.Line2D([x + braces_leg_size, x, x, x + braces_leg_size],
                                [y_bot, y_bot, y_top, y_top],
                                lw=__MATRIX_BRACES_THICKNESS))
    fig.add_artist(lines.Line2D([x_right - braces_leg_size, x_right, x_right, x_right - braces_leg_size],
                                [y_bot, y_bot, y_top, y_top],
                                lw=__MATRIX_BRACES_THICKNESS))

    # Vykreslení prvků matice
    row_n = 0
    for row in items:
        col_n = 0
        for item in row:
            fig.text(
                x=x + brace_space + max_item_len_with_space_scaled * col_n,
                y=y + __CHAR_HEIGHT * row_n,
                s=f"${item}$",
                ha="center",  # Horizontal alignment
            )
            col_n += 1
        row_n += 1

    return x_right - x


def __approx_tex_len(text: str, frac_recursive: bool = True) -> int:
    """:return: Přibližná (přeceněná) délka TeX výrazu. Jednotkou je počet vykreslených číslic (TeX není monospace)."""
    # Vstupní řetězec je postupně upravován a nakonec je změřena jeho délka
    # Krok 1 - Zlomky ve tvaru \frac{Č}{J} nahradit řetězcem o aproximované délce Č nebo J podle toho, co je delší
    if frac_recursive:
        text = re.sub(r"\\frac{([^{}]*)}{([^{}]*)}", __approx_tex_frac_replace, text)
    # Krok 2 - Hledáme výrazy začínající na "\", které jsou po libovolném počtu písmen ukončeny nějakým znakem
    #        - Ty jsou nahrazeny řetězcem "000", důležitá je délka řetězce len("000") == 3
    #        - Některé výrazy (např. \iota) nejsou široké jako tři číslice, lepší ale délku přecenit nežli podcenit
    text = re.sub(r"\\[a-zA-Z]+(?=[^a-zA-Z])", "000", text + " ")
    # Krok 3 - Znaky které jsou širší než číslice, jsou nahrazeny dvouznakovým řetězcem "00"
    for ch in "+-=ABCDEFGHKMNOPQRUVWXYZmw":
        if ch in text:
            text = text.replace(ch, "00")
    # Krok 4 - Znaky " _^{}[]" jsou zahozeny
    text = text.translate(str.maketrans("", "", " _^{}[]"))
    # Krok 5 - Délka upraveného řetězce je vrácena
    return len(text)


def __approx_tex_frac_replace(match: re.Match[str]) -> str:
    numerator_len = __approx_tex_len(match.group(1), False)  # Délka čitatele
    denominator_len = __approx_tex_len(match.group(2), False)  # Délka jmenovatele
    longer_part_len = max(numerator_len, denominator_len)
    return "0" * longer_part_len  # String s délkou odpovídající délce delšího prvku ve zlomku


def __plt_to_image_buffer(buffer: io.BytesIO) -> None:
    """Uloží do byte bufferu `buffer` obrázek s aktuálním matplotlib.pyplot.figure."""
    try:
        plt.savefig(fname=buffer, dpi=__DPI, bbox_inches="tight", pad_inches=0.05, transparent=False)
    finally:
        plt.close()
    buffer.seek(0)
