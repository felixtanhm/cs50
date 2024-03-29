amount = 50

while(amount > 0):
  print(f"Amount Due: {amount}")
  paid = int(input("Insert Coin: ").strip())
  if paid == 25 or paid == 10 or paid == 5: 
    amount -= paid

print(f"Changed Owed: {amount}")