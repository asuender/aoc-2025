import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "./data.txt")


def solve():
    with open(DATA_PATH, "r") as file:
        data = [line.strip() for line in file.readlines()]
        num_rows = len(data)

        current_beams = [data[0].index("S")]
        num_splitters = 0

        for i in range(1, num_rows):
            line = data[i]
            new_beams = []

            for cb in current_beams:
                if line[cb] == "^":
                    num_splitters += 1
                    new_beams.extend([cb - 1, cb + 1])
                else:
                    new_beams.append(cb)

            if new_beams:
                current_beams = list(set(new_beams))

        return num_splitters


if __name__ == "__main__":
    print(solve())
