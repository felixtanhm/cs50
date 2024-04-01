#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int popSize;
    do
    {
        popSize = get_int("Population Starting Size: ");
    }
    while (popSize < 9);
    // TODO: Prompt for end size
    int popEnd;
    do
    {
        popEnd = get_int("Population End Size: ");
    }
    while (popEnd < popSize);

    // TODO: Calculate number of years until we reach threshold
   int years = 0;
   while (popEnd > popSize)
   {
            int newLlamas = popSize / 3;
            int deadLlamas = popSize / 4;
            popSize = popSize + newLlamas - deadLlamas;
            years += 1;
   }
    // TODO: Print number of years
    printf("Years: %d\n", years);
}
