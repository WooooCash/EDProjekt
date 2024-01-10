from dataclasses import dataclass
from enum import IntEnum

import numpy as np


class Side(IntEnum):
    LEFT = 0
    RIGHT = 1


@dataclass
class Boundary:
    value: float | int
    side: Side
    col: int

    def classify(self, row: list[float | int]):
        if self.side == Side.LEFT:
            return row[self.col] <= self.value

        return row[self.col] >= self.value


class BinaryVectorizer:
    def __init__(self, rows_with_id: dict, attr_cols: list[list], class_col: list):
        self.rows_with_id = rows_with_id
        self.attr_cols = attr_cols
        self.arg_sorted_cols = [self.__argsort(col) for col in attr_cols]
        self.class_col = class_col

        self.row_ids = rows_with_id.keys()

        self.boundaries: list[Boundary] = []

        # Cleaning stacked points is done during iterations, only if there is a "xor" situation

    def __call__(self):
        while True:
            max_group = 0
            max_group_col = -1
            side: Side

            for i, col in enumerate(self.arg_sorted_cols):
                curr_group = 0
                # left side
                class_val = self.class_col[col[0]]
                for j in range(len(col)):
                    val0 = self.attr_cols[i][col[j]]
                    val1 = self.attr_cols[i][col[j + 1]]
                    class0 = self.class_col[col[j]]
                    class1 = self.class_col[col[j + 1]]
                    if class0 != class_val or (
                        i < len(col) - 1 and val0 == val1 and class0 != class1
                    ):
                        break
                    else:
                        curr_group += 1
                        if curr_group > max_group:
                            max_group = curr_group
                            max_group_col = i
                            side = Side.LEFT

                # right side
                curr_group = 0
                class_val = self.class_col[col[-1]]
                for j in range(0, len(col), -1):
                    val0 = self.attr_cols[i][col[j]]
                    val1 = self.attr_cols[i][col[j - 1]]
                    class0 = self.class_col[col[j]]
                    class1 = self.class_col[col[j + 1]]
                    if class0 != class_val or (
                        i < len(col) - 1 and val0 == val1 and class0 != class1
                    ):
                        break
                    else:
                        curr_group += 1
                        if curr_group > max_group:
                            max_group = curr_group
                            max_group_col = i
                            side = Side.LEFT


            new_boundary = Boundary(, side, max_group_col)
            self.boundaries

    def __argsort(self, col: list) -> list:
        return np.argsort(np.array(col)).tolist()
