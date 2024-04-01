#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calcIndex(float letters, float words, float sentences);

int main(void)
{
    string text = get_string("Text: ");
    int countedText = count_letters(text);
    int countedWords = count_words(text);
    int countedSentence = count_sentences(text);
    int index = calcIndex((float) countedText, (float) countedWords, (float) countedSentence);
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int count = 0;
    int strlength = strlen(text);
    for (int i = 0; i < strlength; i++)
    {
        char letter = text[i];
        if (isupper(letter) || islower(letter))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1;
    int strlength = strlen(text);
    for (int i = 0; i < strlength; i++)
    {
        char letter = text[i];
        if (letter == 32)
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    int strlength = strlen(text);
    for (int i = 0; i < strlength; i++)
    {
        char letter = text[i];
        if (letter == 33 || letter == 46 || letter == 63)
        {
            count++;
        }
    }
    return count;
}

int calcIndex(float letters, float words, float sentences)
{
    float L = (letters / words) * 100;
    float S = (sentences / words) * 100;
    float index = (0.0588 * L) - (0.296 * S) - 15.8;
    return round(index);
}
