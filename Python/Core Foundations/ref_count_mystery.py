import sys

# 1. Create a brand new object
my_list = ["apple", "banana"] 

# How many tags? Just 'my_list'.
# But getrefcount will say 2.
print(f"Tags pointing to my_list: {sys.getrefcount(my_list)}") 

# 2. Add a second tag
another_tag = my_list

# Now we have 'my_list' and 'another_tag'.
# But getrefcount will say 3.
print(f"Tags pointing to my_list (after adding another_tag): {sys.getrefcount(my_list)}")

# 3. Prove it's the FUNCTION causing the +1
def dummy_function(incoming_tag):
    # 'incoming_tag' is a temporary Post-it note created for this function
    print(f"Inside function, count is: {sys.getrefcount(incoming_tag)}")

print("\nCalling dummy_function...")
dummy_function(my_list) 
# Expect 4! 
# (my_list + another_tag + dummy_function's 'incoming_tag' + getrefcount's internal tag)
