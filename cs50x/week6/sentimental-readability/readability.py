def count_letters(text):
    count = 0
    for letter in text:
        if (letter.isalpha()):
            count += 1
    return count


def count_words(text):
    count = 1
    for character in text:
        if (character == " "):
            count += 1
    return count


def count_sentences(text):
    count = 0
    for character in text:
        if (character in [".", "?", "!"]):
            count += 1
    return count


def calc_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = (0.0588 * L) - (0.296 * S) - 15.8
    return round(index)


textInput = input("Text: ")
letters = count_letters(textInput)
words = count_words(textInput)
sentences = count_sentences(textInput)
index = calc_index(letters, words, sentences)
if (index >= 16):
    print("Grade 16+")
elif (index < 1):
    print("Before Grade 1")
else:
    print(f"Grade {index}")
