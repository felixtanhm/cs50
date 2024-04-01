array = input("Expression: ").strip().split(" ")

match array[1]: 
  case "+": 
    print(float(array[0]) + float(array[2]))
  case "-": 
    print(float(array[0]) - float(array[2]))
  case "*": 
    print(float(array[0]) * float(array[2]))
  case "/": 
    print(float(array[0]) / float(array[2]))
