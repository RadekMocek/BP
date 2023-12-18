import random

import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Inverzní matice"

    def generate_problem(self) -> None:
        # https://math.stackexchange.com/a/19529
        # https://math.stackexchange.com/a/1028487
        values = [-4, -3, -2, -1, 1, 2, 3, 4]
        letters = [random.choice(values) for _ in range(6)]
        mx1 = sp.Matrix([
            [1, letters[0], letters[1]],
            [0, 1, letters[2]],
            [0, 0, 1],
        ])
        mx2 = sp.Matrix([
            [1, 0, 0],
            [letters[3], 1, 0],
            [letters[4], letters[5], 1],
        ])
        mx_init = mx1 * mx2
        mx_inverse = mx_init.inv()

        # TODO: Postup (?)
        # TODO: Lepší output
        # TODO: Output bez $$$

        self.task = f"Vypočítejte inverzní matici k maitici:\n```{sp.pretty(mx_init)}```$$$a"
        self.answer = f"{self.task[:-7]}\n\n{sp.pretty(mx_inverse)}```$$$a"
