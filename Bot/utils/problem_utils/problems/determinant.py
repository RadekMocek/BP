import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Determinant"

    def generate_problem(self) -> None:
        mx = sp.randMatrix(4, min=-2, max=3)
        self.task = f"Vypočítejte determinant matice:```A =\n{sp.pretty(mx)}```"
        self.answer = f"{self.task[:-3]}\n\ndet(A) = {mx.det()}```"
