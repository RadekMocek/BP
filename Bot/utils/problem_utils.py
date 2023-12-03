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

    def generate_problem(self, problem_name: str) -> tuple[str, str, str]:
        return self.problems[problem_name].generate_problem()


class GeneralProblem(ABC):
    @abstractmethod
    def generate_problem(self):
        pass


class MatrixMultiplicationProblem(GeneralProblem):
    def __str__(self) -> str:
        return "Nasobení matic"

    def generate_problem(self) -> str:
        mx1 = np.random.randint(low=-5, high=12, size=(2, 2))
        mx2 = np.random.randint(low=-5, high=12, size=(2, 2))
        mx3 = mx1 @ mx2
        return_task = (f"Vynásobte matice:"
                       f"$$${numpy_array_2_lingebot_matrix(mx1)}\\cdot{numpy_array_2_lingebot_matrix(mx2)}=?")
        return_process = f"Postup..."
        return_answer = numpy_array_2_lingebot_matrix(mx3)
        return return_task  # , return_process, return_answer
