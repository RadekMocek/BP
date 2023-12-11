"""Podpůrný modul pro příklady."""

import pathlib
import random
from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from utils.file_io import txt_read
from utils.text_utils import convert_html_tags

__PROBLEM_FILES_PATH = pathlib.Path(__file__).parent.parent / "_static" / "problems"


def get_problem_tutorial(problem_name: str) -> Optional[str]:
    """:return: Text s návodem pro výpočet dané kategorie příkladů (pokud existuje, jinak None)"""
    return convert_html_tags(txt_read(__PROBLEM_FILES_PATH / f"{problem_name}.MD"))


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
    """Poskytuje generaci příkladů a jejich řešení pro všechny kategorie."""

    def __init__(self) -> None:
        problems_list: list[GeneralProblem] = [
            MatrixMultiplicationProblem(),
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
        dim1 = random.randint(2, 4)
        dim23 = random.randint(2, 4)
        dim4 = random.randint(2, 4)
        mx1 = np.random.randint(low=-5, high=12, size=(dim1, dim23))
        mx2 = np.random.randint(low=-5, high=12, size=(dim23, dim4))
        mx3 = mx1 @ mx2
        self.task = (f"Vynásobte matice:"
                     f"$$${numpy_array_2_lingebot_matrix(mx1)}\\cdot{numpy_array_2_lingebot_matrix(mx2)}=?")
        self.answer = f"{self.task[:-1]}{numpy_array_2_lingebot_matrix(mx3)}"
