# Quick script to highlight all the junctions ("decision points") and slopes in the input

with open("input", "r") as f:
    matrix = [l.strip() for l in f]

print(matrix[0])  # first row has nothing to highlight

for i in range(1, len(matrix)-1):
    for j in range(len(matrix[i])):
        if matrix[i][j] == "#":
            # print walls normally
            print("#", end="")
        elif matrix[i][j] != ".":
            # highlight slopes with coloured background
            print(f"\033[7;35m{matrix[i][j]}\033[0m", end="")
        elif f"{matrix[i-1][j]}{matrix[i+1][j]}{matrix[i][j-1]}{matrix[i][j+1]}".count("#") < 2:
            # highlight decision points as inverse video
            print(f"\033[7m{matrix[i][j]}\033[0m", end="")
        else:
            # print non-decision "." points normally
            print(matrix[i][j], end="")
    print("")

print(matrix[-1])  # last row has nothing to highlight
