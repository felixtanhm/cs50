def calculate_quarters(cents):
    remainder = cents % 25
    quarters = (cents - remainder) / 25
    return int(quarters)


def calculate_dimes(cents):
    remainder = cents % 10
    dimes = (cents - remainder) / 10
    return int(dimes)


def calculate_nickels(cents):
    remainder = cents % 5
    nickels = (cents - remainder) / 5
    return int(nickels)


def calculate_pennies(cents):
    return int(cents)


cents = 0
while cents < 1:
    user_input = input("Change: ")
    if (user_input.replace(".", "", 1).isdigit()):
        user_input = float(user_input)
        if (user_input > 0):
            cents = user_input * 100

quarters = calculate_quarters(cents)
cents = cents - (quarters * 25)
dimes = calculate_dimes(cents)
cents = cents - (dimes * 10)
nickels = calculate_nickels(cents)
cents = cents - (nickels * 5)
pennies = calculate_pennies(cents)

print(quarters + dimes + nickels + pennies)
