"""Podpůrný modul pro příklady."""

import pathlib
from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from utils.file_io import txt_read
from utils.text_utils import convert_html_tags

__PROBLEM_FILES_PATH = pathlib.Path(__file__).parent.parent.parent / "_static" / "problems"


def get_problem_tutorial(problem_name: str) -> Optional[str]:
    """:return: Text s návodem pro výpočet dané kategorie příkladů (pokud existuje, jinak None)"""
    return convert_html_tags(txt_read(__PROBLEM_FILES_PATH / f"{problem_name}.MD"))


def numpy_array_2_lingebot_matrix(array: np.ndarray) -> str:
    result = np.array2string(array, separator=",")
    # → [[1, 2],\n [3, 4]]
    result = "".join(result.split())
    # → [[1,2],[3,4]]
    result = result.replace("],[", ";")
    # → [[1,2;3,4]]
    return result[1:-1]
    # → [1,2;3,4]


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
