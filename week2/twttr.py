string = input("Input: ")
print("Output: ", end="")
for char in string: 
  if char == "a" or char == "e" or char == "i" or char == "o" or char == "u":
    continue
  elif char == "A" or char == "E" or char == "I" or char == "O" or char == "U":
    continue
  else:  
    print(char, sep="", end="")
print("\n", end="")