import os
import numpy as np
from numpy import linalg as LA
from itertools import combinations
from functools import reduce

DATA_PATH = os.path.join(os.path.dirname(__file__), "./data.txt")


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i: int):
        if self.parent[i] == i:
            return i

        return self.find(self.parent[i])

    def unite(self, i: int, j: int):
        i_rep = self.find(i)
        j_rep = self.find(j)

        self.parent[i_rep] = j_rep
        self.size[j_rep] += self.size[i_rep]


def solve():
    with open(DATA_PATH, "r") as file:
        vectors = [tuple(int(x) for x in line.split(",")) for line in file]
        pairs = list(combinations(vectors, 2))
        pairs.sort(key=lambda vp: LA.norm(np.array(vp[0]) - np.array(vp[1])))

        uf = UnionFind(len(vectors))

        for vp in pairs[:1000]:
            v0_idx = vectors.index(vp[0])
            v1_idx = vectors.index(vp[1])

            if uf.find(v0_idx) != uf.find(v1_idx):
                uf.unite(min(v0_idx, v1_idx), max(v0_idx, v1_idx))

        final_sizes = [uf.size[i] for i in range(len(vectors)) if uf.find(i) == i]
        final_sizes.sort(reverse=True)

        return reduce(lambda a, b: a * b, final_sizes[:3])


if __name__ == "__main__":
    print(solve())
