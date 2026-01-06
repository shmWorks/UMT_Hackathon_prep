"""
Lesson 01: Object References and Copying
Topics: Identity (is), Equality (==), Shallow Copy vs Deep Copy.
This script demonstrates how Python handles memory assignment and the 'Variables as Tags' concept.
"""
import copy
'''
Project: “State Inspector”

Write a script that:
==> Creates a nested structure
==> Assigns it to multiple variables
==> Mutates parts
==> Prints id() values
'''
# nested structure
nested_dict = {'names' : ['sheraz'], 'ages' : [22], 'addresses' : [['55'],['B'], ['PUEHS']]}

# assignment 
ref_copied = nested_dict
shallow_copied = nested_dict.copy()
deep_copied = copy.deepcopy(nested_dict)

# 
print(f"ref_copied is nested_dict: {ref_copied is nested_dict}")
print(f"shallow_copied is nested_dict: {shallow_copied is nested_dict}")
print(f"deep_copied is nested_dict: {deep_copied is nested_dict}")

# EVIDENCE: Print the actual memory addresses (IDs)
print(f"ID of nested_dict: {id(nested_dict)}")
print(f"ID of ref_copied:        {id(ref_copied)}")
print(f"ID of shallow_copied:        {id(shallow_copied)}")
print(f"ID of deep_copied:        {id(deep_copied)}")
print(f"All IDs match:     {all(obj is nested_dict for obj in (ref_copied, shallow_copied, deep_copied))}")

# mutation
print("\nMutation\n")

# in nested_dict outer layer
print("\nIn nested_dict outer layer\n")
nested_dict['Phone_No'] = '03100644664'
print(f"nested_dict: {nested_dict}")
print(f"ref_copied: {ref_copied}")   # change reflected as refers to the same object
print(f"shallow_copy: {shallow_copied}")  # not reflected as shallow copy copies the outer layer 
print(f"deep_copy: {deep_copied}")        # not reflected as deep copy copies the entire object

# in nested_dict inner layer
print("\nIn nested_dict inner layer\n")
nested_dict['addresses'][0].append('PUEHS')
print(f"nested_dict: {nested_dict}")
print(f"ref_copied: {ref_copied}")   # change reflected as refers to the same object
print(f"shallow_copy: {shallow_copied}")  # reflected as shallow copy doesn't copy the inner layer 
print(f"deep_copy: {deep_copied}")        # not reflected as deep copy copies the entire object

# in shallow_copied inner layer
print("\nIn shallow_copied inner layer\n")
shallow_copied['addresses'][0].append('PUEHS')
print(f"shallow_copied: {shallow_copied}")
print(f"nested_dict: {nested_dict}")
print(f"ref_copied: {ref_copied}")
print(f"deep_copy: {deep_copied}")

# in deep_copied inner layer
print("\nIn deep_copied inner layer\n")
deep_copied['addresses'][0].append('PUEHS')
print(f"deep_copied: {deep_copied}")
print(f"nested_dict: {nested_dict}")
print(f"ref_copied: {ref_copied}")
print(f"shallow_copy: {shallow_copied}")
