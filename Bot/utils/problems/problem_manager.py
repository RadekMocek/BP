import utils.problems.problem_problems as problems
from utils.problems.problem_utils import GeneralProblem


class ProblemManager:
    """Poskytuje generaci příkladů a jejich řešení pro všechny kategorie."""

    def __init__(self) -> None:
        problems_list: list[GeneralProblem] = [
            problems.MatrixMultiplicationProblem(),
            problems.GaussJordanProblem()
        ]
        self.problems: dict[str, GeneralProblem] = {str(x): x for x in problems_list}

    def get_problems_list(self) -> list[str]:
        """:return: List názvů všech dostupných kategorií příkladů."""
        return list(self.problems.keys())

    def generate_problem(self, problem_name: str) -> tuple[str, str]:
        """:return: Vygenerovaný příklad a řešení příkladu z vybrané kategorie."""
        chosen_problem = self.problems[problem_name]
        chosen_problem.generate_problem()
        return chosen_problem.get_task(), chosen_problem.get_answer()
