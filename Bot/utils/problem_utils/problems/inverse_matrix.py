"""Příklady: Výpočet inverzní matice"""

import sympy as sp

from utils.problem_utils.problem_utils import GeneralProblem, random_det1_33_matrix, sympy_matrices_2_string


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Inverzní matice"

    def generate_problem(self) -> None:
        values = [-4, -3, -2, -1, 1, 2, 3, 4]
        mx_initial = random_det1_33_matrix(values)  # Zadaná matice
        mx_inverse = mx_initial.inv()  # Výsledná matice
        # Matice vypsané v postupu řešení
        mx_process_initial = mx_initial.col_insert(3, sp.eye(3))
        _, _, _, mx_process_gaussed = mx_process_initial.LUdecompositionFF()
        mx_process_final = mx_inverse.col_insert(0, sp.eye(3))
        # Zadání a řešení
        self.task = f"Vypočítejte inverzní matici k matici:\n```A =\n{sp.pretty(mx_initial)}```"
        self.answer = (f"{self.task[:-3]}\n\n"
                       f"{sympy_matrices_2_string([mx_process_initial, mx_process_gaussed, mx_process_final], -3)}\n"
                       f"A⁻¹ =\n{sp.pretty(mx_inverse)}```")
