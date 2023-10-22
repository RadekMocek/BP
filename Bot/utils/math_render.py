import matplotlib.pyplot as plt

from modules.bot import PATH_TEX


def render_tex(text_raw):
    # Obalit text do dolarů, pokud není
    if text_raw[0] == "$" and text_raw[-1] == "$":
        text_math = text_raw
    else:
        text_math = f"${text_raw}$"

    plt.rcParams["mathtext.fontset"] = "cm"

    fig = plt.figure()
    fig.patch.set_facecolor("#323337")
    try:
        fig.text(x=0, y=0, s=text_math, color="white", parse_math=True, usetex=False)
        plt.savefig(fname=PATH_TEX, dpi=280, bbox_inches="tight", pad_inches=0.02, transparent=False)
    finally:
        plt.close()
