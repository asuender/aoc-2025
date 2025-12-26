import os
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    with open(data_path, "r") as file:
        contents = file.read()
        invalid = []

        for r in contents.split(","):
            bounds = r.split("-")
            if bounds:
                lower, upper = bounds
                invalid.extend(
                    [
                        i
                        for i in range(int(lower), int(upper) + 1)
                        if re.fullmatch("([1-9]\\d*)\\1", str(i))
                    ]
                )

        return sum(invalid)


if __name__ == "__main__":
    print(solve())
