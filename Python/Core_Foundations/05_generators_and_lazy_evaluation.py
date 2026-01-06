"""
Lesson 05: Generators and Lazy Evaluation
Topics: yield, next(), Generator Objects, State Retention.
Demystifies the handshake between the Producer (yield) and the Consumer (next).
"""
def coffee_machine():
    print("--- Machine: Starting brew... ---")
    yield "Espresso"  # Pauses here
    
    print("--- Machine: Adding milk... ---")
    yield "Latte"     # Pauses here
    
    print("--- Machine: Adding chocolate... ---")
    yield "Mocha"     # Pauses here
    
    print("--- Machine: Out of beans! ---")

# 1. Calling the function doesn't run it! 
# It just creates the "Generator Object" (the machine is plugged in).
machine = coffee_machine()

# manual way to yield using next()
print("Machine is ready.\n")

# 2. Use next() to get the first yield
print(f"Customer gets: {next(machine)}") 

# 3. Use next() again. It wakes up EXACTLY where it left off.
# Notice it prints "Adding milk..." BEFORE yielding "Latte"
print(f"Customer gets: {next(machine)}")

# 4. One more time
print(f"Customer gets: {next(machine)}")

# 5. What happens if we call next() again?
try:
    next(machine)
except StopIteration:
    print("\n[StopIteration Error]: The generator finished!")


# automatic way to yield using for loop(next(machine) repeatedly called, StopIteration automatically caught)
for i in machine:
    print(i)
