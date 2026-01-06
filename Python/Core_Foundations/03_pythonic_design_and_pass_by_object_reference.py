"""
Lesson 03: Pythonic Design and Pass-by-Object-Reference
Topics: Dynamic Typing, Reference Counting, Function Scoping and Mutation.
Explains the 'Everything is an Object' philosophy and how arguments are passed to functions.
"""
import sys

# --- 1. The "Tag" has no type. The Object has the type. ---
def analyze(tag_name, thing):
    print(f"Tag '{tag_name}' points to -> Type: {type(thing).__qualname__}, Value: {thing}, ID: {id(thing)}")

x = [1, 2]
analyze("x", x)

x = "Now I am a string"
analyze("x", x) # Same tag name, totally different object.


# --- 2. Reference Counting: The connection between Tags and Life ---
# Objects only exist as long as at least one tag points to them.
a = [100, 200, 300]
print(f"\nCreated List {id(a)}. Ref count: {sys.getrefcount(a)}")
# Note: getrefcount is always +1 higher because the function argument itself is a temporary tag!

b = a
print(f"Added tag 'b'. Ref count: {sys.getrefcount(a)}")

b = None 
print(f"Removed tag 'b'. Ref count: {sys.getrefcount(a)}")


# --- 3. The "Function Argument" Reality ---
def modifier(my_tag):
    # my_tag is a COPY of the tag passed in. It points to the SAME object.
    print(f"\nInside Function: my_tag ID seems to be {id(my_tag)}")
    
    # MUTATION: This follows the tag to the object and changes the object.
    my_tag.append("Mutated!")
    
    # REASSIGNMENT: This rips 'my_tag' off the object and puts it on a new one.
    my_tag = [888, 999] 
    print(f"Inside Function: Reassigned my_tag to new ID {id(my_tag)}")

original = [1, 2]
print(f"\nBefore Function: original is {original}, ID: {id(original)}")

modifier(original)

print(f"After Function:  original is {original}")
print("Note: The .append() worked (shared object), but the reassignment to [888, 999] was lost.")
