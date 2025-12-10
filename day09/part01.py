import os
from itertools import combinations

DATA_PATH = os.path.join(os.path.dirname(__file__), "./data.txt")


def solve():
    with open(DATA_PATH, "r") as file:
        points = [tuple(int(x) for x in line.split(",")) for line in file]
        combs = list(combinations(points, 2))

        return max(
            [abs(p1[0] - p2[0] + 1) * abs(p1[1] - p2[1] + 1) for p1, p2 in combs]
        )


if __name__ == "__main__":
    print(solve())
