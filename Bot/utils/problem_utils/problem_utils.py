"""Podpůrný modul pro příklady."""

import pathlib
import random
from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
import sympy as sp

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


def random_det1_22_matrix(values: list[int]) -> sp.Matrix:
    mx1 = sp.Matrix([[1, random.choice(values)], [0, 1]])
    mx2 = sp.Matrix([[1, 0], [random.choice(values), 1]])
    return mx1 * mx2


def random_det1_33_matrix(values: list[int]) -> sp.Matrix:
    # https://math.stackexchange.com/a/19529
    # https://math.stackexchange.com/a/1028487
    letters = [random.choice(values) for _ in range(6)]
    mx1 = sp.Matrix([
        [1, letters[0], letters[1]],
        [0, 1, letters[2]],
        [0, 0, 1],
    ])
    mx2 = sp.Matrix([
        [1, 0, 0],
        [letters[3], 1, 0],
        [letters[4], letters[5], 1],
    ])
    return mx1 * mx2


def sympy_matrices_2_string(matrices: list[sp.Matrix]) -> str:
    n_matrices = len(matrices)
    lines = ["", "", "", "", ""]
    for matrix_index, matrix in enumerate(matrices):
        pretty = sp.pretty(matrix)
        mx_lines = pretty.split("\n")
        for mx_line_index, mx_line in enumerate(mx_lines):
            space = " ~ ... ~ " if mx_line_index == 2 and matrix_index < n_matrices - 1 else "         "
            lines[mx_line_index] += mx_line + space
    result = "".join([f"{x}\n" for x in lines])
    return result


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
