input = input("Greeting: ").lower().strip()

if input.find("hello") == 0: 
  print("$0")
elif input.find("h") == 0: 
  print("$20")
else: 
  print("$100")