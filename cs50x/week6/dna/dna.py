import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    csv_file = sys.argv[1]
    sequence_file = sys.argv[2]

    fieldnames = read_fieldnames(csv_file)
    database = read_data(csv_file)
    sequence = read_sequence(sequence_file)
    str_count = STR_count(sequence, fieldnames[1:])

    match_profile(database, fieldnames[1:], str_count)

    return


def read_fieldnames(file):
    with open(file) as opened_file:
        reader = csv.DictReader(opened_file)
        return reader.fieldnames


def read_data(file):
    rows = []
    with open(file) as opened_file:
        reader = csv.DictReader(opened_file)
        for row in reader:
            rows.append(row)
    return rows


def read_sequence(file):
    sequence = ""
    with open(file) as opened_file:
        sequence = opened_file.read()
    return sequence


def STR_count(sequence, strs):
    count = []
    for str in strs:
        count.append(longest_match(sequence, str))
    return count


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def match_profile(database, fieldnames, str_counts):
    for profile in database:
        match = True
        for i in range(len(fieldnames)):
            if int(profile[fieldnames[i]]) != str_counts[i]:
                match = False
                break

        if match:
            print(profile["name"])
            return
    print("No match")


main()
