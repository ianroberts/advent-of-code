

with open("input", "r") as f:
    print("graph {")
    for line in f:
        line = line.strip()
        src = line[0:3]
        print(f"  {src} -- " + "{" + line[5:] + "}")

    print("}")
