#include <cs50.h>
#include <stdio.h>

int get_height(void);
void print_hash(int height);
void print_row(int tier);

int main(void)
{
    int height = get_height();
    print_hash(height);
}

int get_height(void)
{
    int numeral = 0;
    do
    {
        numeral = get_int("Height: ");
    }
    while (numeral <= 0 || numeral > 8);
    return numeral;
}

void print_hash(int height)
{
    for (int tier = 0; tier < height; tier++)
    {
        // For loop to print the spaces
        for (int spaces = 0; spaces < height - tier - 1; spaces++)
        {
            printf(" ");
        }
        // For loop to print the #
        print_row(tier);
        // Print the space
        printf("  ");
        // For loop to print the #
        print_row(tier);
        printf("\n");
    }
}

void print_row(int tier)
{
    for (int hash = 0; hash < tier + 1; hash++)
    {
        printf("#");
    }
}