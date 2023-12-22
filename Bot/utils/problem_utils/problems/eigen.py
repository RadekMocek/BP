import random

import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, random_det1_matrix


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Vlastní čísla a vektory"

    def generate_problem(self) -> None:
        # https://math.stackexchange.com/a/1377275
        values = [-2, -1, 1, 2]
        mx_v = random_det1_matrix(values)
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
        # TODO
        self.task = f"Určete vlastní čísla a jim odpovídající vlastní vektory matice ```{sp.pretty(mx)}```$$$a"
        self.answer = f"{self.task[:-7]}\n\n{sp.pretty(mx.eigenvals())}\n\n{eigenvectors}```$$$a"
