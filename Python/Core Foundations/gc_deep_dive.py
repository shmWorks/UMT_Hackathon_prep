import gc
import sys

class Node:
    def __init__(self, name):
        self.name = name
        self.child = None
    def __repr__(self):
        return f"Node({self.name})"


# 1. Disable automatic GC for a moment to see the 'leak'
gc.disable()

def create_cycle():
    # Create two nodes
    a = Node("A")
    b = Node("B")
    
    # Link them in a circle (The Zombie Loop)
    a.child = b
    b.child = a
    
    print(f"Inside: Refcount of A = {sys.getrefcount(a)}")
    # When this function ends, tags 'a' and 'b' die.
    # But because they point to each other, refcount stays at 1.

print("--- Step 1: Creating a cycle ---")
create_cycle()

# Force a manual check of ref-counted objects
# (Doesn't show the cycle because refcount is still 1)
print("\n--- Step 2: Cycle created. Objects are unreachable but exist in memory. ---")

# 2. Inspect GC Generations
print(f"GC Objects in Gen 0 before collection: {len(gc.get_objects(generation=0))}")

# 3. Manually trigger the Generational GC
print("\n--- Step 3: Triggering GC Collection ---")
unreachable_count = gc.collect() 
print(f"GC successfully found and destroyed {unreachable_count} unreachable objects.")

# 4. Performance Tuning: The Architect's Lever
# Thresholds: (700, 10, 10) 
# Meaning: Check Gen 0 after 700 allocations. 
# Check Gen 1 after 10 Gen 0 checks.
print(f"\nCurrent GC Thresholds: {gc.get_threshold()}")

# Re-enable GC for safety
gc.enable()
