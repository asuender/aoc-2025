import os
from functools import cache

DATA_PATH = os.path.join(os.path.dirname(__file__), "./data.txt")


def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    with open(data_path, "r") as file:
        data = [line.strip() for line in file.readlines()]

    @cache
    def explore_timeline(start_line, start_beam):
        res = 0
        line = start_line
        beam = start_beam

        found_splitter = False
        while not found_splitter and line < len(data):
            if data[line][beam] == "^":
                left_path = explore_timeline(line + 1, beam - 1)
                right_path = explore_timeline(line + 1, beam + 1)

                if left_path and right_path:
                    res += left_path + right_path

                found_splitter = True

            line += 1

        if line >= len(data):
            return 1

        return res

    return explore_timeline(0, data[0].index("S"))


if __name__ == "__main__":
    print(solve())
