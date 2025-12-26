import os
from itertools import combinations

import numpy as np
from numba import njit

DATA_PATH = os.path.join(os.path.dirname(__file__), "./data.txt")


# Helper functions for visualization


def print_grid(grid: np.ndarray):
    for row in grid:
        print("".join(str(x) for x in row))


def mark_red_between(grid: np.ndarray, t1: tuple[int, int], t2: tuple[int, int]):
    y1, x1 = t1
    y2, x2 = t2

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2)):
            grid[y][x1] = 0
    else:
        for x in range(min(x1, x2), max(x1, x2)):
            grid[y1][x] = 0

    grid[y1][x1] = 0
    grid[y2][x2] = 0


@njit
def do_flood_fill(grid: np.ndarray):
    dims = grid.shape

    for row in range(dims[0]):
        flip = False

        for col in range(dims[1]):
            if grid[row][col] == 0 and not flip:
                flip = True
            elif grid[row][col] == 1 and flip:
                flip = False

            if flip:
                grid[row][min(col + 1, dims[1] - 1)] = 0

# START ai
# The following part has been written using either Gemini 3 Pro
# or CC (can't remember)
@njit
def _flood_fill_kernel(grid):
    """
    Numba-optimized flood fill.
    Assumes grid has a safe '1' border and starts at (0,0).
    0 = Wall/Colored
    1 = Empty
    2 = Outside Water (Temporary)
    """
    rows, cols = grid.shape

    # Pre-allocate a stack. Max size is total pixels.
    # We use a simple array + pointer to simulate a stack.
    stack = np.empty((rows * cols, 2), dtype=np.int32)
    stack_ptr = 0

    # Push start node (0,0)
    stack[stack_ptr, 0] = 0
    stack[stack_ptr, 1] = 0
    stack_ptr += 1

    # Mark (0,0) as Outside Water (2)
    grid[0, 0] = 2

    # Directions: Up, Down, Left, Right
    # (Using manual unrolling or a small array is fine)
    dr = np.array([-1, 1, 0, 0])
    dc = np.array([0, 0, -1, 1])

    while stack_ptr > 0:
        # Pop
        stack_ptr -= 1
        r = stack[stack_ptr, 0]
        c = stack[stack_ptr, 1]

        # Check neighbors
        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]

            # Boundary checks
            if 0 <= nr < rows and 0 <= nc < cols:
                # If it is empty space (1), fill it with water (2)
                if grid[nr, nc] == 1:
                    grid[nr, nc] = 2

                    # Push to stack
                    stack[stack_ptr, 0] = nr
                    stack[stack_ptr, 1] = nc
                    stack_ptr += 1

    # Post-processing:
    # Any '1' left is 'Inside' (dry land) -> convert to 0 (valid colored tile)
    # Any '2' is 'Outside' -> convert back to 1 (empty space)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                grid[r, c] = 0  # Fill the inside!
            elif grid[r, c] == 2:
                grid[r, c] = 1  # Reset outside to empty


def fill_interior(grid: np.ndarray):
    """
    Python wrapper that handles padding.
    """
    # 1. Pad the grid with a border of 1s (empty space)
    # This ensures the flood fill can travel around the shape
    # even if the shape touches the edges.
    padded_grid = np.pad(grid, pad_width=1, mode="constant", constant_values=1)

    # 2. Run the Numba kernel
    _flood_fill_kernel(padded_grid)

    # 3. Unpad (remove the border) and update the original grid
    # We copy the result back into the original grid structure
    filled_interior = padded_grid[1:-1, 1:-1]

    # Copy data back to your original reference if needed,
    # or just return filled_interior.
    np.copyto(grid, filled_interior)
# END ai

@njit
def do_check_outer(
    grid: np.ndarray, tiles: tuple[tuple[int, int], tuple[int, int]]
) -> bool:
    t1, t2 = tiles

    row_min = min(t1[0], t2[0])
    row_max = max(t1[0], t2[0])
    col_min = min(t1[1], t2[1])
    col_max = max(t1[1], t2[1])

    left_upper = [row_min, col_min]
    width = col_max - col_min
    height = row_max - row_min

    current = left_upper

    # go to the right
    for x in range(width + 1):
        if grid[current[0]][current[1]] == 1:
            return False
        current[1] += 1
    current[1] -= 1

    # go down
    for x in range(height + 1):
        if grid[current[0]][current[1]] == 1:
            return False
        current[0] += 1
    current[0] -= 1

    # go left
    for x in range(width + 1):
        if grid[current[0]][current[1]] == 1:
            return False
        current[1] -= 1
    current[1] += 1

    # go up
    for x in range(height + 1):
        if grid[current[0]][current[1]] == 1:
            return False
        current[0] -= 1

    return True


def solve(data_path: str | None = None):
    if data_path is None:
        data_path = DATA_PATH

    with open(data_path, "r") as file:
        reds = [(int(line.split(",")[1]), int(line.split(",")[0])) for line in file]
        grid_size = (
            max([tile[0] for tile in reds]) + 1,
            max([tile[1] for tile in reds]) + 1,
        )

        grid = np.ones(grid_size, dtype=np.int8)

        print(f"Grid size is {grid_size}")

        for i in range(len(reds)):
            t1 = reds[i]
            t2 = reds[(i + 1) % len(reds)]

            mark_red_between(grid, t1, t2)

        # We now assume that the first red tile in the list represents
        # the "upper-left" corner

        print("Starting flood fill...")
        fill_interior(grid)

        print("Checking rectangles...")
        rects = list(
            filter(lambda pair: do_check_outer(grid, pair), list(combinations(reds, 2)))
        )

        return max(
            [(abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1) for t1, t2 in rects]
        )


if __name__ == "__main__":
    print(solve())
