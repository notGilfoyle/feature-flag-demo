from mmh3 import hash

SIZE = 20
bits = [0] * SIZE


def add(item):
    for seed in range(3):
        idx = hash(item, seed) % SIZE
        bits[idx] = 1


def contains(item):
    for seed in range(3):
        idx = hash(item, seed) % SIZE
        if bits[idx] == 0:
            return False
    return True


add("apple")
add("banana")

print(contains("apple"))   # True (probably)
print(contains("orange"))  # False (definitely not)