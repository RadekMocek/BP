"""Příklady: Výpočet vlastních čísel a vektorů"""

import random

import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, random_det1_22_matrix, sympy_matrix_pretty


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Vlastní čísla a vektory"

    def generate_problem(self) -> None:
        # Vygenerovat matici, jejíž vlastní čísla jsou celá (https://math.stackexchange.com/a/1377275)
        # (Alternativní řešení: https://math.stackexchange.com/a/2389199)
        values = [-2, -1, 1, 2]
        mx_v = random_det1_22_matrix(values)
        mx_a = sp.Matrix([
            [random.randint(-10, 10), 0],
            [0, random.randint(-10, 10)],
        ])
        mx = mx_v * mx_a * mx_v.inv()
        # Zadání
        self.task = f"Určete vlastní čísla a jim odpovídající vlastní vektory matice:\n```{sp.pretty(mx)}```"
        # Výpočet charakteristického polynomu (pouze pro ukázání v postupu řešení)
        lambda_symbol = sp.symbols("lambda")
        characteristic_mx = mx.copy()
        characteristic_mx[0] -= lambda_symbol
        characteristic_mx[3] -= lambda_symbol
        characteristic_polynom_str = sp.pretty(characteristic_mx.det()) + " = 0"
        # Vlastní čísla dosazená do matice za lambdu (pouze pro ukázání v postupu řešení)
        eigenvalues = ""
        for eigenvalue in reversed(mx.eigenvals().keys()):
            eigenvalues += f"\nVlastní číslo {eigenvalue}:\n"
            eigenvalue_mx = mx.copy()
            eigenvalue_mx[0] -= eigenvalue
            eigenvalue_mx[3] -= eigenvalue
            eigenvalue_mx = eigenvalue_mx.col_insert(2, sp.Matrix([0, 0]))
            eigenvalues += f"{sympy_matrix_pretty(eigenvalue_mx, -1)}\n"
        # Řetězec vlastních čísel a jim odpovídajícím vlastním vektorům
        eigenvectors = ""
        for tup in mx.eigenvects():
            eigenvectors += f"  Vlastní číslo: {tup[0]}\nVlastní vektory: {[list(x) for x in tup[2]]}\n\n"
        # Řešení
        self.answer = (f"{self.task[:-3]}"
                       f"\n\n{sp.pretty(characteristic_mx)}\n\n{characteristic_polynom_str}"
                       f"\n\n{eigenvalues}"
                       f"\n\n{eigenvectors}"
                       f"```")
