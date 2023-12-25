from utils.problem_utils.problem_utils import GeneralProblem


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Ortogonalizace"

    def can_generate_problem(self) -> bool:
        return False

    def generate_problem(self) -> None:
        pass
