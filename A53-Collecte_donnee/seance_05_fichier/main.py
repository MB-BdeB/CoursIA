with open("tot.txt") as fin:
    lines = fin.readlines()

# sort the lines by length in descending order
    lines = sorted(lines, key=lambda x: len(x), reverse=True)

# print the first 10 lines along with their lengths
    for line in lines:
        print(line)