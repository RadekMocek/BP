import random

import numpy as np
import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Soustavy rovnic"

    def generate_problem(self) -> None:
        x, y, z = (random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))

        rows = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
        ])

        rows_iter1 = np.array([
            np.add(rows[0], rows[2] * random.randint(-4, 4)),
            np.add(rows[1], rows[0] * random.randint(-4, 4)),
            np.add(rows[2], rows[1] * random.randint(-4, 4)),
        ])

        rows_iter2 = np.array([
            np.add(rows_iter1[0], rows_iter1[1] * random.randint(-4, 4)),
            np.add(rows_iter1[1], rows_iter1[2] * random.randint(-4, 4)),
            np.add(rows_iter1[2], rows_iter1[0] * random.randint(-4, 4)),
        ])
        equations = "".join([f"{x[0]}x+{x[1]}y+{x[2]}z&={x[3]}\\\\" for x in rows_iter2])
        equations = equations.replace("+-", "-")
        self.task = f"Vypočítejte soustavu rovnic:$$${equations}"

        mx_initial = sp.Matrix(rows_iter2)
        _, _, _, mx_gaussed = mx_initial.LUdecompositionFF()
        mx_final = sp.Matrix(rows)

        # TODO: Vydělit řádky matice U nejvyšším společným dělitelem daného řádku
        # TODO: Vertikální oddělovač pravé strany
        # TODO: Vypsat sympy matice vedle sebe
        # TODO: Příklady typu lin.komb., případně mx1*mx?=mx2
        # TODO: Postup (?)

        self.answer = (f"```{sp.pretty(mx_initial)}\n\n{sp.pretty(mx_gaussed)}\n\n{sp.pretty(mx_final)}```"
                       f"$$$x&={x}\\\\y&={y}\\\\z&={z}")
