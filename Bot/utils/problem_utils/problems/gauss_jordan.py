import math
import random

import numpy as np
import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, sympy_matrices_2_string


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Soustavy rovnic"

    def mx_row_gcd(self, row):
        row_gcd = math.gcd(*row)
        return [0 if row_gcd == 0 else element // row_gcd for element in row]

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

        # Vydělit řádky matice nejvyšším společným dělitelem daného řádku
        mx_gaussed = sp.Matrix([self.mx_row_gcd(row) for row in mx_gaussed.tolist()])

        # TODO: Vertikální oddělovač pravé strany
        # TODO: Příklady typu lin.komb., případně mx1*mx?=mx2
        # TODO: Postup (?)

        self.answer = (f"```{sympy_matrices_2_string([mx_initial, mx_gaussed, mx_final])}"
                       f"\n\nx = {x}\ny = {y}\nz = {z}```")
