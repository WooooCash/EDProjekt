from typing import Callable, Optional

import numpy as np


class Data:
    def __init__(self) -> None:
        self.__reset()

    def read_file(self, file, delimiter: str, has_headers: bool):
        self.__reset()

        if has_headers:
            self.headers = ["ID", *process_line(file.readline(), delimiter)]

        first_line = file.readline()
        first_row = process_line(first_line, delimiter)
        first_row = [1, *parse_ints(first_row)]
        self.col_count = len(first_row)

        self.__add_row(first_row)

        for i, line in enumerate(file.readlines()):
            row = process_line(line, delimiter)
            row = [i + 2, *parse_ints(row)]
            self.__add_row(row)

        file.close()

        if not has_headers:
            self.headers = ["ID", *[f"col{i}" for i in range(1, self.col_count)]]

    def __reset(self):
        self.headers: list = []
        self.cols: list = []
        self.col_count: int = 0

    def __add_row(self, row: list):
        if not self.cols:
            self.cols.extend([] for i in range(self.col_count))

        if len(row) != self.col_count:
            raise RowLengthError(f"Row has wrong number of columns ({len(row)}).")

        for i, el in enumerate(row):
            self.cols[i].append(el)

    def process_column(self, col_idx: int, operation: Callable, config: dict = {}):
        self.cols[col_idx] = operation(self.cols[col_idx], config)

    def get_headers(self):
        return self.headers[1:]

    def as_rows(self, col_selection: Optional[list[int]] = None) -> tuple[list, dict]:
        """Returns a tuple of row data list and a column mapping dict which can be ignored if col_selection is not passed"""
        cols = self.cols[1:]
        col_mapping = {i: i for i in range(len(cols))}
        if col_selection:
            cols = [col for i, col in enumerate(cols) if i in col_selection]
            col_mapping = {i: orig_idx for i, orig_idx in enumerate(col_selection)}

        rows = np.array(self.cols[1:]).T
        return rows.tolist(), col_mapping

    def as_rows_id(
        self, col_selection: Optional[list[int]] = None
    ) -> tuple[dict, dict]:
        """Returns a tuple of a dict mapping id to row data and a column mapping which can be ignored if col_selection is not passed"""
        rows_data, col_mapping = self.as_rows(col_selection)
        return {id: data for id, data in zip(self.cols[0], rows_data)}, col_mapping

    def __str__(self):
        disp_str = " | ".join(self.headers) + "\n"
        disp_str += "---\n"
        row_len = len(self.cols[0])

        for i in range(row_len):
            disp_str += " | ".join([str(col[i]) for col in self.cols])
            disp_str += "\n"

        return disp_str


class RowLengthError(ValueError):
    def __init__(self, msg, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg


def process_line(line: str, delimiter: str) -> list[str]:
    return [el.strip() for el in line.split(delimiter) if el]


def parse_ints(row: list[str]):
    parsed_row = []

    for el in row:
        try:
            val = int(el)
        except ValueError:
            val = el
        parsed_row.append(val)

    return parsed_row
