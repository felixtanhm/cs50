#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BYTEBLOCK 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    // Declare jpg file variable
    FILE *jpeg;
    // Create buffer for data block
    uint8_t buffer[BYTEBLOCK];
    char *file_name = malloc(8);
    int count = 0;

    while (fread(buffer, 1, BYTEBLOCK, input) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Close current jpg before opening new one
            if (count > 0)
                fclose(jpeg);
            // Create and open new jpg
            sprintf(file_name, "%03i.jpg", count);
            jpeg = fopen(file_name, "w");
            if (jpeg == NULL)
            {
                printf("Could not open file.\n");
                return 1;
            }

            count++;
            fwrite(buffer, 1, BYTEBLOCK, jpeg);
        }
        else if (count > 0)
            fwrite(buffer, 1, BYTEBLOCK, jpeg);
    }
    fclose(jpeg);
    fclose(input);
    free(file_name);
}
