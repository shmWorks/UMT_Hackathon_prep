# --- 1. The "Box" Illusion (Immutable Objects) ---
# Integers are immutable. You can't change the number 10. 
# You can only move the tag to a different number.

a = 10
b = a

print(f"Start: a is {a}, b is {b}")
print(f"Address of a: {id(a)}")
print(f"Address of b: {id(b)}") # Same address! Both tags on the object (10)

# "Changing" b
b = 20 
# WAIT! You didn't change the object 10 into 20. 
# You ripped the tag 'b' off 10 and stuck it on a new object 20.

print("\nAfter b = 20:")
print(f"a is {a} (Still on the old object)")
print(f"b is {b} (Now on a new object)")


# --- 2. The "Tag" Reality (Mutable Objects) ---
# Lists are mutable. You CAN change the object itself.

list_a = [1, 2, 3]
list_b = list_a # Stick a second tag on the SAME list

print(f"\n\nStart Lists: list_a is {list_a}, list_b is {list_b}")
print(f"Address of list_a: {id(list_a)}")
print(f"Address of list_b: {id(list_b)}") # EXACT SAME ADDRESS

# We modify the OBJECT through tag 'list_b'
list_b.append(999)

print("\nAfter list_b.append(999):")
print(f"list_b is {list_b}")
print(f"list_a is {list_a}  <-- LOOK! list_a changed too!")

# This proves: We didn't copy the box. We just shared the object.
