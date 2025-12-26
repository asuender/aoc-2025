import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    ranges = []

    with open(data_path, "r") as file:
        for line in file.readlines():
            if not line.strip():
                break

            a, b = line.split("-")
            ranges.append((int(a), int(b)))

    # Sort ranges by start position
    ranges.sort()

    merged = []
    for start, end in ranges:
        if not merged or merged[-1][1] < start:
            merged.append((start, end))
        else:
            last_start, last_end = merged[-1]
            merged[-1] = (last_start, max(end, last_end))

    total_count = 0
    for start, end in merged:
        total_count += end - start + 1

    return total_count


if __name__ == "__main__":
    print(solve())
