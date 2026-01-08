"""
PHASE 3: Error Handling & Debugging
Goal: distinct exceptions, preventing silent failures, and "X-ray" logging.

------------------------------------------------------------------
EXERCISE 1: The "Fragile" Agent (Specific Exceptions)
------------------------------------------------------------------
Agents interact with unstable worlds (APIs, files, users).
You must catch SPECIFIC errors. Catching 'Exception' hides bugs.
"""

def mock_llm_call(prompt):
    # Simulates different failures
    if "network" in prompt:
        raise ConnectionError("API Timeout")
    if "context" in prompt:
        raise ValueError("Context length exceeded")
    return "Success"

def safe_generate(prompt):
    # CHALLENGE 1:
    # Wrap the call in a try/except block.
    # 1. Catch ConnectionError -> Print "Retrying..." and return None.
    # 2. Catch ValueError -> Print "Shortening context..." and return None.
    # 3. DO NOT catch other errors (let them crash so you see them).
    
    # result = mock_llm_call(prompt) # <--- FIX THIS
    # return result
    pass 

print("--- Exercise 1: Specific Catching ---")
# safe_generate("network failure")
# safe_generate("context too long")

"""
------------------------------------------------------------------
EXERCISE 2: The "Silent Killer" (Pass is Evil)
------------------------------------------------------------------
Never write an empty 'except' block. It hides typos and logic errors.
"""

def process_data(data):
    try:
        # Imagine a typo here, e.g., calling a method that doesn't exist
        return data.processs() # Typo: 'processs' instead of 'process'
    except:
        # bad practice: This swallows the AttributeError!
        pass 
    return "Default"

# CHALLENGE 2:
# 1. Run this. It returns "Default", hiding the bug.
# 2. Change 'except:' to 'except Exception as e:' and PRINT the error.
# 3. Observe the crash report (Traceback).

class MockData:
    def process(self): return "Processed"

print("\n--- Exercise 2: Silent Failures ---")
# print(process_data(MockData()))

"""
------------------------------------------------------------------
EXERCISE 3: Transitions to Logging (No more Print)
------------------------------------------------------------------
In production/hackathons, you can't stare at the console. 
You need logs to file.
"""
import logging

# Basic Config - Run this ONCE at the start of your program
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def complex_chain(input_text):
    # CHALLENGE 3:
    # Replace print() with logging.info() and logging.error()
    print(f"Received input: {input_text}")
    
    if not input_text:
        print("Error: Empty input!")
        return
        
    print("Processing...")
    # Simulate work
    print("Done.")

print("\n--- Exercise 3: Logging ---")
complex_chain("Hello Agent")
complex_chain("")


def risky_tool_call(input_data):
    # Simulate a crash
    raise ValueError("API Connection Failed")

# --- BAD WAY ---
# result = risky_tool_call("data") 
# CRASH! The program ends here.

# --- AGENTIC WAY ---
try:
    result = risky_tool_call("data")
except Exception as e:
    # We catch the crash and turn it into text
    print(f"Log: Tool failed with error: {e}")
    result = "Error: The tool failed to connect. Please try a different method."

# The program continues! 
# The LLM receives the string "Error..." and thinks: "Okay, I'll try Google Search instead."