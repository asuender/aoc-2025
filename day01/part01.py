import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")

def solve():
  dial = 50
  count_dial_zero = 0

  with open(DATA_PATH, "r") as file:
      for line in file.readlines():
          dir = line[0]
          by = int(line[1:])

          dial = dial + by if dir == "R" else dial - by
          dial %= 100

          if dial == 0:
              count_dial_zero += 1

      return count_dial_zero

if __name__ == "__main__":
    print(solve())