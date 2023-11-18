import pytest

from src.preprocessing import to_numeric


class TestPreprocessing:
    @pytest.mark.parametrize(
        "input_col,expected_col",
        [
            (["one", "two", "three"], [0, 1, 2]),
            (["one", "one", "three"], [0, 0, 1]),
            (["one", "one", "one"], [0, 0, 0]),
            (["one", "two", "two"], [0, 1, 1]),
        ],
    )
    def test_to_numeric(self, input_col, expected_col):
        output_col = to_numeric(input_col, {})

        assert len(output_col) == len(input_col)
        assert output_col == expected_col
