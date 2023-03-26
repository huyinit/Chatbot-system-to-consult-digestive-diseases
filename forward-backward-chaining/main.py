import os

from chaining.backward_chaining import BackwardChaining
from chaining.forward_chaining import ForwardChaining

program = "BC"


# program = "FC"


'''
while True:
    print("Do you want to use Forward or Backward chaining?")
    print("FC - Forward chaining")
    print("BC - Backward chaining")
    program = input()
    if program == "FC" or program == "BC":
        break
    print("Incorrect choice.")
'''
#file_name = r"D:\7\forward-backward-chaining\forward-backward-chaining\ex"

file_name = r"ex"

'''
while True:
    file_name = input("Enter file name:\n")
    if os.path.isfile(file_name):
        break
    else:
        print("File not found.")
'''

if program == "FC":
    ForwardChaining(file_name)
if program == "BC":
    BackwardChaining(file_name)
#D:\7\forward-backward-chaining\forward-backward-chaining\res\bc\1