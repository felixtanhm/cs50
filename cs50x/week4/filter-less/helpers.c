#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int i = 0;

    while (i < height)
    {
        int j = 0;

        while (j < width)
        {
            float total = image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen;
            int avg = round(total / 3.0);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
            j++;
        }
        i++;
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int i = 0;

    while (i < height)
    {
        int j = 0;

        while (j < width)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen +
                                 .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen +
                                   .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen +
                                  .131 * image[i][j].rgbtBlue);

            if (sepiaRed > 255)
                sepiaRed = 255;
            if (sepiaGreen > 255)
                sepiaGreen = 255;
            if (sepiaBlue > 255)
                sepiaBlue = 255;

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
            j++;
        }
        i++;
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int iterations = width / 2;
    int i = 0;
    while (i < height)
    {
        int j = 0;
        while (j < iterations)
        {
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
            j++;
        }
        i++;
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    int i = 0;

    while (i < height)
    {
        int j = 0;
        while (j < width)
        {
            copy[i][j] = image[i][j];
            j++;
        }
        i++;
    }

    i = 0;
    while (i < height)
    {
        int j = 0;
        while (j < width)
        {
            float red = 0;
            float green = 0;
            float blue = 0;

            int i_start = i - 1;
            int i_end = i + 1;

            int count = 0;

            if (i == 0)
                i_start = 0;
            if (i == height - 1)
                i_end = height - 1;

            while (i_start <= i_end)
            {
                int j_start = j - 1;
                int j_end = j + 1;

                if (j == 0)
                    j_start = 0;
                if (j == width - 1)
                    j_end = width - 1;

                while (j_start <= j_end)
                {
                    red += copy[i_start][j_start].rgbtRed;
                    green += copy[i_start][j_start].rgbtGreen;
                    blue += copy[i_start][j_start].rgbtBlue;
                    count++;
                    j_start++;
                }
                i_start++;
            }
            red = round(red / count);
            green = round(green / count);
            blue = round(blue / count);
            if (red > 255)
                red = 255;
            if (green > 255)
                green = 255;
            if (blue > 255)
                blue = 255;
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
            j++;
        }
        i++;
    }
    return;
}
