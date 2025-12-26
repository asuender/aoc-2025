import os
from functools import reduce

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    with open(data_path, "r") as file:
        content = file.readlines()
        res = 0

        number_lines = content[:-1]
        op_line = content[-1]

        op = op_line[0]
        nums = []
        is_separator = False
        for i in range(len(op_line)):
            nums_s = "".join([nl[i] for nl in number_lines if nl[i].strip()])
            if nums_s:
                nums.append(int(nums_s))

            is_separator = not bool(nums_s)
            on_last_column = i == len(op_line) - 1

            if on_last_column or is_separator:
                if op == "+":
                    res += sum(nums)
                else:
                    res += reduce(lambda a, b: a * b, nums)

                op = op_line[min(i + 1, len(op_line) - 1)]
                nums = []

    return res


if __name__ == "__main__":
    print(solve())
