#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string input);
int rotate(char character, int key);

int main(int argc, string argv[])
{
    if (argc != 2 || only_digits(argv[1]))
    {
        printf("Please input a single positive integer.\n");
        return 1;
    }
    int key = atoi(argv[1]);
    string plainText = get_string("Plaintext: ");

    printf("ciphertext: ");

    int strlength = strlen(plainText);
    for (int i = 0; i < strlength; i++)
    {
        int rotatedChar = rotate(plainText[i], key);
        printf("%c", rotatedChar);
    }
    printf("\n");
}

bool only_digits(string input)
{
    int count = 0;
    int strlength = strlen(input);
    for (int i = 0; i < strlength; i++)
    {
        char character = input[i];
        if (character > 57 || character < 48)
        {
            return true;
        }
    }
    return false;
}

int rotate(char character, int key)
{
    if (islower(character))
    {
        character -= 97;
        character += key;
        character = 97 + character % 26;
    }
    if (isupper(character))
    {
        character -= 65;
        character += key;
        character = 65 + character % 26;
    }
    return character;
}