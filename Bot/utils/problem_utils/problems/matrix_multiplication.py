"""Příklady: Násobení matic"""

import random

import numpy as np

from utils.problem_utils.problem_utils import GeneralProblem, numpy_array_2_lingebot_matrix as mx


class Problem(GeneralProblem):
    def __str__(self) -> str:
        return "Nasobení matic"

    def generate_problem(self) -> None:
        # Náhodné dimenze matic, roumezí 2–4
        dim1 = random.randint(2, 4)
        dim23 = random.randint(2, 4)
        dim4 = random.randint(2, 4)
        # Šířka první matice musí být stejná jako výška té druhé
        mx1 = np.random.randint(low=-5, high=12, size=(dim1, dim23))
        mx2 = np.random.randint(low=-5, high=12, size=(dim23, dim4))
        # NumPy maticové násobení se zapisuje pomocí zavináče
        mx3 = mx1 @ mx2
        self.task = f"Vynásobte matice:$$${mx(mx1)}\\cdot{mx(mx2)}=?"
        self.answer = f"{self.task[:-1]}{mx(mx3)}"
