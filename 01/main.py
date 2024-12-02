# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from heapq import heapify, heappush, heappop

if __name__ == "__main__":
    heap_left = []
    heap_right = []
    heapify(heap_left)
    heapify(heap_right)

    with open("data.txt", "r", encoding="utf-8") as f:
        while line := f.readline():
            l, r = line.rstrip().split("   ")
            heappush(heap_left, int(l))
            heappush(heap_right, int(r))
    distance = 0
    while heap_left or heap_right:
        min_l = heappop(heap_left)
        min_r = heappop(heap_right)
        distance += abs(min_l - min_r)
    print(f"final distance is {distance}")
