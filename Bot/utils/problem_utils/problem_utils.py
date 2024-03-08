"""Podpůrný modul pro příklady."""

import pathlib
import random
import re
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
    """:return: Řetězec s NumPy maticí převedenou do formátu pro LingeBot vykreslení"""
    result = np.array2string(array, separator=",")
    # → [[1, 2],\n [3, 4]]
    result = "".join(result.split())
    # → [[1,2],[3,4]]
    result = result.replace("],[", ";")
    # → [[1,2;3,4]]
    return result[1:-1]
    # → [1,2;3,4]


def random_det1_22_matrix(values: list[int]) -> sp.Matrix:
    """:param values: Z tohoto listu se vybírají hodnoty pro generaci:
    Velikost čísel ovlivní velikost čísel ve výsledné matici
    :return: Náhodná 2x2 matice mx, kde det(mx)==1"""
    mx1 = sp.Matrix([[1, random.choice(values)], [0, 1]])
    mx2 = sp.Matrix([[1, 0], [random.choice(values), 1]])
    return mx1 * mx2


def random_det1_33_matrix(values: list[int]) -> sp.Matrix:
    """:param values: Z tohoto listu se vybírají hodnoty pro generaci:
    Velikost čísel ovlivní velikost čísel ve výsledné matici
    :return: Náhodná 3x3 matice mx, kde det(mx)==1"""
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


def sympy_matrix_pretty(mx: sp.Matrix, vertical_line_col_index: int = 0) -> str:
    """:param mx: SymPy matice
    :param vertical_line_col_index: Pozice vertikální čáry, indexuje se odzadu (záporné číslo; 0==bez čáry)
    :return: Pretty printed SymPy matice s volitelnou vertikální čárou"""
    pretty = sp.pretty(mx)
    if vertical_line_col_index >= 0 or -vertical_line_col_index >= mx.shape[1]:
        return pretty
    # Prvky ve sloupcích SymPy matice jsou zarovnány na střed, je tedy potřeba projet všechny řádky
    # a najít správný index, na který lze umístit vertikální čáru, aniž by protínala nějaký prvek
    pretty_lines = pretty.split("\n")
    pattern = re.compile(r"\s(?=\S)")  # Hledat mezeru následovanou znakem
    vertical_line_position = len(pretty)
    for line in pretty_lines:
        matches = [x.start() for x in pattern.finditer(line[1:-1])]
        if not matches:
            continue
        index = matches[vertical_line_col_index] + 1
        if index < vertical_line_position:
            vertical_line_position = index
    return "\n".join([x[:vertical_line_position] + "⎥" + x[vertical_line_position:] for x in pretty_lines])


def sympy_matrices_2_string(matrices: list[sp.Matrix], separator: str, vertical_line_col_index: int = 0) -> str:
    """:return: Řetězec s pretty printed SymPy maticemi napsanými vedle sebe
    a oddělenými `separator`; volitelná vertikální čára"""
    empty_space = " " * len(separator)
    n_matrices = len(matrices)
    lines = []
    first_iter = True
    for matrix_index, matrix in enumerate(matrices):
        pretty = sympy_matrix_pretty(matrix, vertical_line_col_index)
        mx_lines = pretty.split("\n")
        for mx_line_index, mx_line in enumerate(mx_lines):
            if mx_line_index == int(len(mx_lines) / 2) and matrix_index < n_matrices - 1:
                space = separator
            else:
                space = empty_space
            if first_iter:
                lines.append(mx_line + space)
            else:
                lines[mx_line_index] += mx_line + space
        first_iter = False
    result = "".join([f"{x}\n" for x in lines])
    return result


class GeneralProblem(ABC):
    """Z této abstraktní třídy dědí všechny ostatní třídy pro generaci příkladů."""

    def __init__(self):
        self.task, self.answer = ("",) * 2

    def get_task(self) -> str:
        return self.task

    def get_answer(self) -> str:
        return self.answer

    def can_generate_problem(self) -> bool:
        return True

    @abstractmethod
    def generate_problem(self) -> None:
        pass
