import random

import numpy as np
import sympy as sp

from utils.problems.problem_utils import GeneralProblem, numpy_array_2_lingebot_matrix as mx


class MatrixMultiplicationProblem(GeneralProblem):
    def __str__(self) -> str:
        return "Nasobení matic"

    def generate_problem(self) -> None:
        dim1 = random.randint(2, 4)
        dim23 = random.randint(2, 4)
        dim4 = random.randint(2, 4)
        mx1 = np.random.randint(low=-5, high=12, size=(dim1, dim23))
        mx2 = np.random.randint(low=-5, high=12, size=(dim23, dim4))
        mx3 = mx1 @ mx2
        self.task = (f"Vynásobte matice:"
                     f"$$${mx(mx1)}\\cdot{mx(mx2)}=?")
        self.answer = f"{self.task[:-1]}{mx(mx3)}"


class GaussJordanProblem(GeneralProblem):
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

        self.answer = (f"```{sp.pretty(mx_initial)}\n\n{sp.pretty(mx_gaussed)}\n\n{sp.pretty(mx_final)}```"
                       f"$$$x&={x}\\\\y&={y}\\\\z&={z}")
