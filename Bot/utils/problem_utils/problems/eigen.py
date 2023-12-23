import random

import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, random_det1_22_matrix, random_det1_33_matrix


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Vlastní čísla a vektory"

    def generate_problem(self) -> None:
        self.eigen_22()

    def eigen_22(self) -> None:
        values = [-2, -1, 1, 2]
        mx_v = random_det1_22_matrix(values)
        mx_a = sp.Matrix([
            [random.randint(-10, 10), 0],
            [0, random.randint(-10, 10)],
        ])
        mx = mx_v * mx_a * mx_v.inv()

        eigenvectors = []
        for tup in mx.eigenvects():
            for vector in tup[2]:
                eigenvectors.append(list(vector))

        self.task = f"Určete vlastní čísla a jim odpovídající vlastní vektory matice\n```{sp.pretty(mx)}```"

        lambda_symbol = sp.symbols("lambda")
        character_mx = mx.copy()
        character_mx[0] -= lambda_symbol
        character_mx[3] -= lambda_symbol
        character_pol_str = sp.pretty(character_mx.det()) + " = 0"
        # TODO

        self.answer = (f"{self.task[:-3]}"
                       f"\n\n{sp.pretty(character_mx)}\n\n{character_pol_str}"
                       f"\n\n{sp.pretty(mx.eigenvals())}\n\n{eigenvectors}"
                       f"```")

    def eigen_33(self) -> None:
        # https://math.stackexchange.com/a/1377275
        values = [-2, -1, 1, 2]
        mx_v = random_det1_33_matrix(values)
        eigenvalues = [random.randint(-10, 10) for _ in range(3)]
        mx_a = sp.Matrix([
            [eigenvalues[0], 0, 0],
            [0, eigenvalues[1], 0],
            [0, 0, eigenvalues[2]],
        ])
        mx = mx_v * mx_a * mx_v.inv()

        eigenvectors = []
        for tup in mx.eigenvects():
            for vector in tup[2]:
                eigenvectors.append(list(vector))
        self.task = f"Určete vlastní čísla a jim odpovídající vlastní vektory matice ```{sp.pretty(mx)}```"
        self.answer = f"{self.task[:-3]}\n\n{sp.pretty(mx.eigenvals())}\n\n{eigenvectors}```"
