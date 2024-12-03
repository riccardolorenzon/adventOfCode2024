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

    with open("data.txt", "r", encoding="utf-8") as f:
        while line := f.readline():
            l, r = line.rstrip().split("   ")
            heappush(heap_left, int(l))
            heappush(heap_right, int(r))

    similarity_score = 0
    similarity_cache = {}
    while heap_left:
        element = heappop(heap_left)
        if similarity_cache.get(element):
            pass
        else:
            while heap_right and heap_right[0] < element:
                heappop(heap_right)
            while heap_right and heap_right[0] == element:
                similarity_cache[element] = similarity_cache.get(element, 0) + element
                heappop(heap_right)
        similarity_score += similarity_cache.get(element, 0)

    print(f"final similarity_score is {similarity_score}")
