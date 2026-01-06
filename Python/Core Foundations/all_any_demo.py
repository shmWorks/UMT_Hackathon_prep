# The Truthiness Checklist
results = [True, True, False]

print(f"all(results): {all(results)}")  # False (because of one False)
print(f"any(results): {any(results)}")  # True (because at least one is True)

# --- PRACTICAL EXAMPLES ---

# 1. Validation: Are all user inputs valid?
inputs = ["admin", "password123", "email@test.com"]
is_valid = all(len(i) > 0 for i in inputs)
print(f"All fields filled: {is_valid}")

# 2. Search: Are there any even numbers?
nums = [1, 3, 5, 8, 9]
has_even = any(n % 2 == 0 for n in nums)
print(f"Contains an even number: {has_even}")

# 3. Short-circuiting:
# any() stops at the first True. all() stops at the first False.
def slow_check(x):
    print(f"Checking {x}...")
    return x > 0

print("Testing any() short-circuit:")
any(slow_check(i) for i in [1, -5, 10]) # Will stop after checking '1'

# --- THE "ANY + VALUE" PATTERN ---

# 4. Search and Capture: Find the first even number
nums = [1, 3, 5, 8, 9, 10]
first_even = next((n for n in nums if n % 2 == 0), "No evens found")

print(f"\nFirst even value: {first_even}")

# Why use next()? 
# It's as efficient as any() because it stops (short-circuits) 
# exactly at the first match.
