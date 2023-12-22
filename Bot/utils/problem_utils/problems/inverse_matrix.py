import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, random_det1_matrix


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Inverzní matice"

    def generate_problem(self) -> None:
        values = [-4, -3, -2, -1, 1, 2, 3, 4]
        mx_init = random_det1_matrix(values)
        mx_inverse = mx_init.inv()

        # TODO: Postup (?)
        # TODO: Lepší output
        # TODO: Output bez $$$

        self.task = f"Vypočítejte inverzní matici k maitici:\n```{sp.pretty(mx_init)}```$$$a"
        self.answer = f"{self.task[:-7]}\n\n{sp.pretty(mx_inverse)}```$$$a"
