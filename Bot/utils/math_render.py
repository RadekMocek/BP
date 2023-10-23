import io
import re

import matplotlib.lines as lines
import matplotlib.pyplot as plt

__COLOR_BACKGROUND = "#323337"  # Barva pozadí Discord chatu ve výchozím nastavení
__COLOR_FOREGROUND = "white"  # Barva písma pro tmavé pozadí
__MATRIX_SPACE_SCALE = 0.02  # Velikost mezer mezi prvky matice
__MATRIX_SPACE_VERTICAL_MULTIPLIER = 2.2
__MATRIX_MIN_ITEM_LEN_MULTIPLIER = 1.2
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
    min_item_len = __MATRIX_SPACE_SCALE * __MATRIX_MIN_ITEM_LEN_MULTIPLIER  # Vynásobeno pro lepší vzhled úzkých matic
    max_item_len = min_item_len  # Délka nejdelšího prvku matice
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

            item_len = __approx_tex_len(item) * __MATRIX_SPACE_SCALE
            if item_len > max_item_len:
                max_item_len = item_len
        items.append(row_items)

        n_cols = len(cols)
        if n_cols > max_n_cols:
            max_n_cols = n_cols

    # Závorky matice – zjištění rohových bodů
    max_item_len_half = max_item_len / 2
    x_left = -max_item_len_half
    x_right = ((max_n_cols - 1) * max_item_len) + max_item_len_half
    n_rows = len(rows)
    y_top = __MATRIX_SPACE_VERTICAL_MULTIPLIER * __MATRIX_SPACE_SCALE * n_rows
    y_bot = -__MATRIX_SPACE_SCALE

    # Pokud je matice příliš úzká, přizpůsobit tvar závorek (více odsadit a zkrátit "nožky")
    braces_leg_size = __MATRIX_SPACE_SCALE
    if max_item_len == min_item_len or max_n_cols * max_item_len <= 2 * braces_leg_size:
        braces_leg_size /= 2
        x_left -= max_item_len_half
        x_right += max_item_len_half

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
                x=max_item_len * col_n,
                y=__MATRIX_SPACE_VERTICAL_MULTIPLIER * __MATRIX_SPACE_SCALE * row_n,
                s=f"${item}$",
                ha="center",  # Horizontal alignment
            )
            col_n += 1
        row_n += 1

    return __plt_to_image_buffer()


def __approx_tex_len(text: str) -> int:
    """Vrací PŘIBLIŽNOU délku TeX výrazu (přibližný počet znaků po vykreslení, vrací více než méně)."""
    text = text.replace("\\frac", "")
    text = text.replace("\\", " \\")
    text = re.sub(r"\\[^\\\s{_^()\[]*[\\\s{_^()\[]", "0", text + " ")
    text = text.translate(str.maketrans("", "", " _^{}[]"))
    return len(text)


def __plt_to_image_buffer() -> io.BytesIO:
    """Vrací byte buffer s uloženým obrázkem aktuální matplotlib.pyplot.figure."""
    buf = io.BytesIO()
    plt.savefig(fname=buf, dpi=200, bbox_inches="tight", pad_inches=0.02, transparent=False)
    plt.close()
    buf.seek(0)
    return buf
