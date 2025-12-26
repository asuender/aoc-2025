import os
import re
from functools import reduce

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    with open(data_path, "r") as file:
        content = file.readlines()
        res = 0

        nums = [
            [int(x) for x in re.findall("\\d+", line)]
            for line in content[: len(content) - 1]
        ]

        operations = re.findall("\\*|\\+", content[len(content) - 1])

        for i in range(len(operations)):
            column = [row[i] for row in nums]
            if operations[i] == "+":
                res += sum(column)
            else:
                res += reduce(lambda a, b: a * b, column)

    return res


if __name__ == "__main__":
    print(solve())
