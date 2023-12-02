"""Podpůrný modul pro výklad příklady."""
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
        self.problems: list[GeneralProblem] = [
            MatrixMultiplication(),
        ]

    def list_problems(self) -> list[str]:
        return [str(x) for x in self.problems]


class GeneralProblem(ABC):
    @abstractmethod
    def generate_problem(self) -> tuple[str, str, str]:  # -> Zadání, Postup, Výsledek
        pass


class MatrixMultiplication(GeneralProblem):
    def __str__(self) -> str:
        return "Nasobení matic"

    def generate_problem(self) -> tuple[str, str, str]:
        mx1 = np.random.randint(low=-5, high=12, size=(2, 2))
        mx2 = np.random.randint(low=-5, high=12, size=(2, 2))
        mx3 = mx1 @ mx2
        return_task = (f"Vynásbote matice:"
                       f"$$${numpy_array_2_lingebot_matrix(mx1)}\\cdot{numpy_array_2_lingebot_matrix(mx2)}=?")
        return_process = f"Postup..."
        return_answer = numpy_array_2_lingebot_matrix(mx3)
        return return_task, return_process, return_answer
