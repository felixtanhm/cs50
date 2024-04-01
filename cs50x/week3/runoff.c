#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
} candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    int i = 0;

    while (candidates[i].name != NULL)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            preferences[voter][rank] = i;
            return true;
        }
        i++;
    }
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    int index = 0;
    int rank = 0;

    while (index < voter_count)
    {
        rank = 0;
        while (rank < candidate_count)
        {
            int c_index = preferences[index][rank];

            if (!candidates[c_index].eliminated)
            {
                candidates[c_index].votes++;
                break;
            }
            rank++;
        }
        index++;
    }

    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    int treshold = voter_count / 2;
    int i = 0;

    while (candidates[i].name != NULL)
    {
        if (candidates[i].votes > treshold)
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
        i++;
    }

    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    int votes = voter_count;
    int i = 0;

    while (candidates[i].name != NULL)
    {
        if (candidates[i].votes < votes && !candidates[i].eliminated)
            votes = candidates[i].votes;
        i++;
    }

    return votes;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    int i = 0;

    while (candidates[i].name != NULL)
    {
        if (candidates[i].votes > min)
            return false;
        i++;
    }

    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    int i = 0;

    while (candidates[i].name != NULL)
    {
        if (candidates[i].votes == min)
            candidates[i].eliminated = true;
        i++;
    }

    return;
}

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int index = 0; index < voter_count; index++)
    {

        // Query for each rank
        for (int rank = 0; rank < candidate_count; rank++)
        {
            string name = get_string("Rank %i: ", rank + 1);

            // Record vote, unless it's invalid
            if (!vote(index, rank, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}
