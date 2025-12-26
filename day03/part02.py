import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def max_joltage_greedy(bank, k=12):
    bank = bank.strip()
    n = len(bank)
    if k >= n:
        return int(bank)

    result = []
    to_skip = n - k

    for i in range(n):
        while result and to_skip > 0 and result[-1] < bank[i]:
            result.pop()
            to_skip -= 1

        result.append(bank[i])

    return int("".join(result[:k]))


def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    with open(data_path, "r") as file:
        res = []

        for line in file.readlines():
            max_comb = max_joltage_greedy(line, k=12)
            res.append(max_comb)

        return sum(res)


if __name__ == "__main__":
    print(solve())
