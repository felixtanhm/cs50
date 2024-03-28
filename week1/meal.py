def main():
    time = input("What time is it? ").strip()
    num = convert(time)
    if num >= 7 and num <= 8:
      print("breakfast time")
    if num >= 12 and num <= 13:
      print("lunch time")
    if num >= 18 and num <= 19:
      print("dinner time")


def convert(time):
    array = time.split(":")
    hour = float(array[0])
    min = float(array[1]) / 60
    return hour + min


if __name__ == "__main__":
    main()