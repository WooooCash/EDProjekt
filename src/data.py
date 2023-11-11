import numpy as np


class Data:
    headers: list = []
    data: np.array

    def read_file(self, file, delimiter: str, has_headers: bool):
        if has_headers:
            self.headers = process_line(file.readline(), delimiter)

        first_line = file.readline()
        first_row = process_line(first_line, delimiter)
        first_row = parse_ints(first_row)

        self.data = np.array([], shape=(0, len(first_row)))
        self.__add_row(first_row)

        for line in file.readlines():
            row = process_line(line, delimiter)
            row = parse_ints(row)
            self.__add_row(row)

        file.close()

    def __add_row(self, row: list):
        try:
            self.data = np.append(self.data, [row], axis=0)
        except ValueError:
            raise RowLengthError("Row has wrong number of columns.")


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
