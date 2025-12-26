import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")

def zeros_during_move(start_dial: int, dir: str, by: int):
    sign = -1 if dir == "L" else 1

    k0 = (-sign * start_dial) % 100
    first_zero = 100 if k0 == 0 else k0

    if first_zero > by:
        return 0

    return 1 + (by - first_zero) // 100

def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    dial = 50
    count_dial_zero = 0

    with open(data_path, "r") as file:
        for line in file.readlines():
            dir = line[0]
            by = int(line[1:])

            count_dial_zero += zeros_during_move(dial, dir, by)

            sign = -1 if dir == "L" else 1
            dial = (dial + sign * by) % 100

    return count_dial_zero

if __name__ == "__main__":
    print(solve())