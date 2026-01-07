"""
CONCEPT PROOF: Mutable Default Arguments
---------------------------------------------------------
The Question: 
"Is a new default made every time... or the exact same object retained?"

The Answer: 
The EXACT SAME object is retained.

Let's prove it using Python's built-in `id()` function, 
which acts like a memory address pointer.
"""

def guilty_function(name, unique_id=object(), shared_list=[]):  # use none instead of a mutatable object as default ==> shared_list=None
    """
    Args:
        name: Just a label for the call.
        unique_id: A trick to show a NEW object is created if we use the right pattern.
                   (We won't focus on this yet, just look at shared_list).
        shared_list: The dangerous mutable default.
    """
    print(f"--- Call: {name} ---")
    
    # Check the memory address of the list
    address = id(shared_list)
    print(f"Memory Address of 'shared_list': {address}")
    
    # Modify it
    shared_list.append(name)
    print(f"Current Content: {shared_list}")
    print(f"Functions's __defaults__: {guilty_function.__defaults__}")
    print("")

dictionary = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}

# Scalable, Professional Method: Data-Driven Formatting
# We define WHAT we want to show, then use ONE loop to define HOW to show it.
sections = [
    ("Keys", dictionary.keys()),
    ("Values", dictionary.values()),
    ("Key-Value Pairs", [f"{k}:{v}" for k, v in dictionary.items()])
]

for label, data in sections:
    # 1. map(str, data) ensures everything is a string
    # 2. ', '.join() puts commas ONLY between items (no trailing comma)
    # 3. f-string handles the layout and the newline automatically
    print(f"{label}: {', '.join(map(str, data))}")


print("DEFINING FUNCTION NOW...")
# At this exact nanosecond, the list [] is created ONE TIME.
# It is stored inside 'guilty_function' itself.

print("CALLING A...")
guilty_function("A")

print("CALLING B...")
guilty_function("B")

print("CALLING C...")
guilty_function("C")

"""
EXPLANATION:
1. Python executes the `def` line only ONCE.
2. It evaluates `[]` -> creates a List Object (let's call it List_123).
3. It attaches List_123 to the function object.
4. Every time you call the function, if you don't provide a list, 
   Python hands you List_123.
"""
