import random
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
    cl: int

    def classify(self, row: list[float | int]):
        if self.side == Side.LEFT:
            return int(row[self.col] <= self.value)

        return int(row[self.col] >= self.value)

    def __str__(self):
        return f"val: {self.value}, side: {self.side}, col: {self.col}, class: {self.cl}"


class BinaryVectorizer:
    def __init__(
        self, rows_with_id: dict, attr_cols: list[list], class_col: list, id_col: list
    ):
        self.rows_with_id = rows_with_id
        self.attr_cols = attr_cols
        self.arg_sorted_cols = [self.__argsort(col) for col in attr_cols]
        self.class_col = class_col
        self.id_col = id_col

        self.row_ids = rows_with_id.keys()

        self.boundaries: list[Boundary] = []

        self.removed_points = []
        self.removed_point_count = 0

        self.__remove_points()

        self.initial_count = len(self.class_col)

        # Cleaning stacked points is done during iterations, only if there is a "xor" situation

    def __call__(self) -> list[Boundary]:
        # TODO: FIX INFINITE LOOPING WHEN GETS STUCK ON SECOND IF (maybe cleaning stacked points?)
        while True:
            max_group = 0
            max_group_col = -1
            max_group_class = -1
            val = 0
            side: Side = Side.LEFT

            visited_rows = []

            for i, col in enumerate(self.arg_sorted_cols):
                curr_group = 0
                # left side
                class_val = self.class_col[col[0]]
                for j in range(len(col)):
                    val0 = self.attr_cols[i][col[j]]
                    class0 = self.class_col[col[j]]
                    if class0 != class_val:
                        break
                    elif j < len(col) - 1:
                        val1 = self.attr_cols[i][col[j + 1]]
                        class1 = self.class_col[col[j + 1]]
                        visited_rows.extend([col[j], col[j + 1]])
                        if val0 == val1 and class0 != class1:
                            break

                    curr_group += 1
                    if curr_group > max_group:
                        max_group = curr_group
                        max_group_col = i
                        side = Side.LEFT
                        val = val0
                        max_group_class = class0

                # right side
                curr_group = 0
                class_val = self.class_col[col[-1]]
                for j in range(len(col) - 1, -1, -1):
                    val0 = self.attr_cols[i][col[j]]
                    class0 = self.class_col[col[j]]
                    if class0 != class_val:
                        break
                    elif j > 0:
                        val1 = self.attr_cols[i][col[j - 1]]
                        class1 = self.class_col[col[j - 1]]
                        visited_rows.extend([col[j], col[j - 1]])
                        if val0 == val1 and class0 != class1:
                            break

                    curr_group += 1
                    if curr_group > max_group:
                        max_group = curr_group
                        max_group_col = i
                        side = Side.RIGHT
                        val = val0
                        max_group_class = class0

            if max_group < 1:
                row_to_remove = random.choice(visited_rows)
                row_id = self.id_col[row_to_remove]
                self.__remove_rows([row_to_remove])
                self.removed_points.append(row_id)
                self.removed_point_count += 1
                print(f"No boundary could be set. Removing row {row_to_remove}.")
                continue

            new_boundary = Boundary(val, side, max_group_col, max_group_class)
            self.boundaries.append(new_boundary)
            print(new_boundary)

            # Removing appropriate rows
            col = self.arg_sorted_cols[max_group_col]
            rows_to_remove = (
                col[:max_group]
                if side == Side.LEFT
                else col[len(col)-max_group:]
            )
            self.__remove_rows(rows_to_remove)

            row_count = len(self.class_col)
            print(f"{row_count}/{self.initial_count} rows left to cluster")

            if len(self.class_col) == 0:
                break

        print(f"Created a total of {len(self.boundaries)} boundaries for binary vector")
        print(self.boundaries)
        print(
            f"Removed {self.removed_point_count} points. {self.initial_count-self.removed_point_count} remain."
        )
        return self.boundaries

    def __argsort_cols(self):
        self.arg_sorted_cols = [self.__argsort(col) for col in self.attr_cols]

    def __argsort(self, col: list) -> list:
        return np.argsort(np.array(col)).tolist()

    def __remove_rows(self, indices: list[int]):
        self.attr_cols = np.delete(np.array(self.attr_cols), indices, -1).tolist()
        self.class_col = self.__del_indices(self.class_col, indices)
        print(f"Deleting ids: {[self.id_col[i] for i in indices]}")
        self.id_col = self.__del_indices(self.id_col, indices)

        # resort to update all  other cols
        self.__argsort_cols()

    def __del_indices(self, col: list, indices: list) -> list:
        return np.delete(np.array(col), indices).tolist()

    def __remove_points(self):
        pass
