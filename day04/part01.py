import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")


def solve():
    matrix = []
    with open(DATA_PATH, "r") as file:
        for line in file.readlines():
            line_list = list(line)
            line_list.pop()
            matrix.append(line_list)

        width = len(matrix[0])
        height = len(matrix)

        accessable = []

        for i in range(height):
            for j in range(width):
                if matrix[i][j] != "@":
                    continue

                neighbours_idx = [
                    (-1, 0),
                    (-1, 1),
                    (0, 1),
                    (1, 1),
                    (1, 0),
                    (1, -1),
                    (0, -1),
                    (-1, -1),
                ]

                num_neighbours = 0
                for n_idx in neighbours_idx:
                    n_i = i + n_idx[0]
                    n_j = j + n_idx[1]

                    if n_i < 0 or n_i >= height or n_j < 0 or n_j >= width:
                        continue

                    if matrix[n_i][n_j] == "@":
                        num_neighbours += 1

                if num_neighbours < 4:
                    accessable.append((i, j))

        for a in accessable:
            matrix[a[0]][a[1]] = "x"

        # return "\n".join(["".join(d for d in line) for line in matrix])
        return len(accessable)


if __name__ == "__main__":
    print(solve())
