import sys

# Compare a list,tuple,set with the same items
# integers from 1-100000000 in each data structure
items = list(range(1, 10000000))
l = list(items)
t = tuple(items)
s = set(items)

print(f"Memory of List:  {sys.getsizeof(l)} bytes")
print(f"Memory of Tuple: {sys.getsizeof(t)} bytes")
print(f"Memory of Set:   {sys.getsizeof(s)} bytes")

# Efficiency in all()
# 1. List (Small overhead for dynamic resizing)
all(x > 0 for x in [1, 2, 3])

# 2. Tuple (Optimized for static collections)
all(x > 0 for x in (1, 2, 3))
