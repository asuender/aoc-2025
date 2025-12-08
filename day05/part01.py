import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def solve():
    ranges = []
    switch_to_ids = False
    num_fresh = 0

    with open(DATA_PATH, "r") as file:
        for line in file.readlines():
            if not line.strip():
                switch_to_ids = True
                continue

            if not switch_to_ids:
                a, b = line.split("-")
                ranges.append((int(a), int(b)))
            else:
                x = int(line)
                for r in ranges:
                    a, b = r
                    if x >= a and x <= b:
                        num_fresh += 1
                        break

        return num_fresh


if __name__ == "__main__":
    print(solve())
