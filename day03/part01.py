import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def solve():
    with open(DATA_PATH, "r") as file:
        res = []

        for line in file.readlines():
            digits = list(line)[:-1]
            tmp = []

            for i in range(len(digits)):
                d = digits[i]

                combs = [int(d + digits[j]) for j in range(i + 1, len(digits))]
                tmp.append(max(combs) if combs else 0)

            res.append(max(tmp))

        return sum(res)


if __name__ == "__main__":
    print(solve())
