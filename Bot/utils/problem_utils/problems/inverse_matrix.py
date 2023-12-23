import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, random_det1_33_matrix


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Inverzní matice"

    def generate_problem(self) -> None:
        values = [-4, -3, -2, -1, 1, 2, 3, 4]
        mx_init = random_det1_33_matrix(values)
        mx_inverse = mx_init.inv()

        # TODO: Postup (?)
        # TODO: Lepší output

        self.task = f"Vypočítejte inverzní matici k maitici:\n```{sp.pretty(mx_init)}```"
        self.answer = f"{self.task[:-3]}\n\n{sp.pretty(mx_inverse)}```"
