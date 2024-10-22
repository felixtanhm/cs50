def print_row(tier):
    print("#" * (tier + 1), end="")


def print_hash(height):
    for tier in range(height):
        print(" " * (height - tier - 1), end="")
        print_row(tier)
        print("  ", end="")
        print_row(tier)
        print()


height = 0
while height < 1 or height > 8:
    user_input = input("Height: ")
    if (user_input.isdigit()):
        height = int(user_input)
print_hash(height)
