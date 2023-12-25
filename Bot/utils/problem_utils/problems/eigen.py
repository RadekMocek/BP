import random

import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, random_det1_22_matrix, sympy_matrix_pretty


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Vlastní čísla a vektory"

    def generate_problem(self) -> None:
        # Vygenerovat matici, jejíž vlastní čísla jsou celá (https://math.stackexchange.com/a/1377275)
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
        character_mx = mx.copy()
        character_mx[0] -= lambda_symbol
        character_mx[3] -= lambda_symbol
        character_pol_str = sp.pretty(character_mx.det()) + " = 0"
        # Vlastní čísla dosazená do matice za lambdu (pouze pro ukázání v postupu řešení)
        eigenvalues = ""
        for num in reversed(mx.eigenvals().keys()):
            eigenvalues += f"\nVlastní číslo {num}:\n"
            num_mx = mx.copy()
            num_mx[0] -= num
            num_mx[3] -= num
            num_mx = num_mx.col_insert(2, sp.Matrix([0, 0]))
            eigenvalues += f"{sympy_matrix_pretty(num_mx,-1)}\n"
        # Řetězec vlastních čísel a jim odpovídajícím vlastním vektorům
        eigenvectors = ""
        for tup in mx.eigenvects():
            eigenvectors += f"  Vlastní číslo: {tup[0]}\nVlastní vektory: {[list(x) for x in tup[2]]}\n\n"
        # Řešení
        self.answer = (f"{self.task[:-3]}"
                       f"\n\n{sp.pretty(character_mx)}\n\n{character_pol_str}"
                       f"\n\n{eigenvalues}"
                       f"\n\n{eigenvectors}"
                       f"```")

    """
    def eigen_33(self) -> None:
        values = [-2, -1, 1, 2]
        mx_v = random_det1_33_matrix(values)
        eigenvalues = [random.randint(-10, 10) for _ in range(3)]
        mx_a = sp.Matrix([
            [eigenvalues[0], 0, 0],
            [0, eigenvalues[1], 0],
            [0, 0, eigenvalues[2]],
        ])
        mx = mx_v * mx_a * mx_v.inv()
    """
