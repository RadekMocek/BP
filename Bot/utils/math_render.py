import io
import re

import matplotlib.lines as lines
import matplotlib.pyplot as plt

__DPI = 180
__COLOR_BACKGROUND = "#323337"  # Barva pozadí Discord chatu ve výchozím nastavení
__COLOR_FOREGROUND = "white"  # Barva písma pro tmavé pozadí
__MATRIX_CHAR_WIDTH = 0.011  # Šířka krátkého znaku v matici
__MATRIX_SPACE_WIDTH = 0.02  # Šířka mezery v matici
__MATRIX_SPACE_VERTICAL_MULTIPLIER = 2.2  # Výška mezery v matici = šířka * tato konstanta
__MATRIX_BRACES_THICKNESS = 0.75  # Tloušťka závorek vykreslené matice

plt.rcParams["text.usetex"] = False  # Nepoužívat lokální TeX distribuci, ale Matplotlib renderer
plt.rcParams["text.parse_math"] = True
plt.rcParams["text.color"] = __COLOR_FOREGROUND
plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern


def render_tex(text_raw: str) -> io.BytesIO:
    """Vrací byte buffer obrázek s vykresleným TeX výrazem."""
    # Obalit text do dolarů, pokud není
    if text_raw[0] == "$" and text_raw[-1] == "$":
        text_math = text_raw
    else:
        text_math = f"${text_raw}$"
    # O vykreslení matematického výrazu se stará Matplotlib
    fig = plt.figure()
    fig.patch.set_facecolor(__COLOR_BACKGROUND)
    fig.text(x=0, y=0, s=text_math)
    # Obrázek není třeba ukládat lokálně, je uložen do byte bufferu a rovnou odeslán
    return __plt_to_image_buffer()


def render_matrix(text: str) -> io.BytesIO:
    """Vrací byte buffer obrázek s vykreslenou maticí."""
    fig = plt.figure()
    fig.patch.set_facecolor(__COLOR_BACKGROUND)

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
    matrix_space_height = __MATRIX_SPACE_VERTICAL_MULTIPLIER * __MATRIX_SPACE_WIDTH

    # Závorky matice – zjištění rohových bodů
    brace_space = (max_item_len * __MATRIX_CHAR_WIDTH / 2) + __MATRIX_CHAR_WIDTH
    x_left = -brace_space
    x_right = max_item_len_with_space_scaled * (max_n_cols - 1) + brace_space
    y_top = matrix_space_height * len(rows)
    y_bot = -__MATRIX_SPACE_WIDTH

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
                x=max_item_len_with_space_scaled * col_n,
                y=matrix_space_height * row_n,
                s=f"${item}$",
                ha="center",  # Horizontal alignment
            )
            col_n += 1
        row_n += 1

    return __plt_to_image_buffer()


def __approx_tex_len(text: str) -> int:
    """Vrací PŘIBLIŽNOU délku TeX výrazu, jednotkou je počet krátkých znaků (Mathtext není monospace)."""
    text = text.replace("\\frac", "")
    text = text.replace("\\", " \\")
    for ch in "+-ABCDEFGHKMNOPQRUVWXYZmw":
        if ch in text:
            text = text.replace(ch, "00")
    text = re.sub(r"\\[^\\\s{_^()\[]*[\\\s{_^()\[]", "0", text + " ")
    text = text.translate(str.maketrans("", "", " _^{}[]"))
    return len(text)


def __plt_to_image_buffer() -> io.BytesIO:
    """Vrací byte buffer s uloženým obrázkem aktuální matplotlib.pyplot.figure."""
    buf = io.BytesIO()
    plt.savefig(fname=buf, dpi=__DPI, bbox_inches="tight", pad_inches=0.02, transparent=False)
    plt.close()
    buf.seek(0)
    return buf
