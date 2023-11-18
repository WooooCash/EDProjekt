class Data:
    def __init__(self) -> None:
        self.__reset()

    def read_file(self, file, delimiter: str, has_headers: bool):
        self.__reset()

        if has_headers:
            self.headers = process_line(file.readline(), delimiter)

        first_line = file.readline()
        first_row = process_line(first_line, delimiter)
        first_row = parse_ints(first_row)
        self.col_count = len(first_row)

        self.__add_row(first_row)

        for line in file.readlines():
            row = process_line(line, delimiter)
            row = parse_ints(row)
            self.__add_row(row)

        file.close()

        if not has_headers:
            self.headers = [f"col{i}" for i in range(1, self.col_count + 1)]

    def __reset(self):
        self.headers: list = []
        self.cols: list = []
        self.col_count: int = 0

    def __add_row(self, row: list):
        if not self.cols:
            self.cols.extend([] for i in range(self.col_count))

        if len(row) != self.col_count:
            raise RowLengthError(f"Row has wrong number of columns ({len(row)}).")

        print("ROW", row)
        for i, el in enumerate(row):
            self.cols[i].append(el)

    def __str__(self):
        disp_str = " | ".join(self.headers) + "\n"
        disp_str += "---\n"
        row_len = len(self.cols[0])
        print("ROW_LEN", row_len)
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
