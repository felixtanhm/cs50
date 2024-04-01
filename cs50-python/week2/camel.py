string = input("camelCase: ")
print("snake_case: ", end="")
for char in string: 
  if char.isupper():
    print("_" + char.lower(), sep="", end="")
  else: 
    print(char, sep="", end="")
print("\n", end="")