

def first_marker(num_chars):
    with open("input", "r") as f:
        data = f.read().strip()

    for i in range(num_chars, len(data)+1):
        if len(set(data[i-num_chars:i])) == num_chars:
            return i


if __name__ == "__main__":
    print(f"First marker: {first_marker(4)}")
    print(f"First message marker: {first_marker(14)}")