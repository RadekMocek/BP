"""Podpůrný modul pro příklady."""

from abc import ABC, abstractmethod

import numpy as np


def numpy_array_2_lingebot_matrix(array: np.ndarray) -> str:
    # → [[1, 2],\n [3, 4]]
    result = np.array2string(array, separator=",")
    # → [[1,2],[3,4]]
    result = "".join(result.split())
    # → [[1,2;3,4]]
    result = result.replace("],[", ";")
    # → [1,2;3,4]
    return result[1:-1]


class ProblemManager:
    def __init__(self) -> None:
        problems_list: list[GeneralProblem] = [
            MatrixMultiplicationProblem(),
        ]
        self.problems: dict[str, GeneralProblem] = {str(x): x for x in problems_list}

    def list_problems(self) -> list[str]:
        return list(self.problems.keys())

    def generate_problem(self, problem_name: str) -> tuple[str, str]:
        chosen_problem = self.problems[problem_name]
        chosen_problem.generate_problem()
        return chosen_problem.get_task(), chosen_problem.get_answer()


class GeneralProblem(ABC):
    def __init__(self):
        self.task, self.answer = ("",) * 2

    def get_task(self) -> str:
        return self.task

    def get_answer(self) -> str:
        return self.answer

    @abstractmethod
    def generate_problem(self) -> None:
        pass


class MatrixMultiplicationProblem(GeneralProblem):
    def __str__(self) -> str:
        return "Nasobení matic"

    def generate_problem(self) -> None:
        mx1 = np.random.randint(low=-5, high=12, size=(2, 2))
        mx2 = np.random.randint(low=-5, high=12, size=(2, 2))
        mx3 = mx1 @ mx2
        self.task = (f"Vynásobte matice:"
                     f"$$${numpy_array_2_lingebot_matrix(mx1)}\\cdot{numpy_array_2_lingebot_matrix(mx2)}=?")
        self.answer = f"{self.task[:-1]}{numpy_array_2_lingebot_matrix(mx3)}"
