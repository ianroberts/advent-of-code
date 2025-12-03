

def ranges(start, end):
    if len(start) == len(end):
        if len(start) % 2 == 0:
            yield start, end, len(start) // 2
    else:  # len(start) < len(end)
        if len(start) % 2 == 0:
            yield start, str(10**len(start) - 1), len(start) // 2
        start = str(10**len(start))
        for i in range(len(start), len(end)):
            if i % 2 == 1:
                yield str(10**i), str((10**i+1) - 1), (i + 1) // 2
        if len(end) % 2 == 0:
            yield str(10**(len(end)-1)), end, len(end) // 2

def main():
    with open("input", "r") as f:
        data = [tuple(pair.split("-", maxsplit=1)) for pair in f.readline().strip().split(",")]

    total_repeated = 0
    for start, end in data:
        for l, r, length in ranges(start, end):
            lchunks = [int(l[i:i+length]) for i in range(0, len(l), length)]
            rchunks = [int(r[i:i+length]) for i in range(0, len(r), length)]

            ll = lchunks[0]
            for lr in lchunks[1:]:
                if ll < lr:
                    ll += 1
            rl = rchunks[0]
            for rr in rchunks[1:]:
                if rl > rr:
                    rl -= 1

            if rl < ll:
                # no valid repetitions in this range
                continue

            # the repeated numbers are
            # sum(x from ll to rl) * (sum(10**(length*i)) for i from 0 to (len(l)/length)-1)
            #
            # sum(x from ll to rl) = sum(x from 1 to rl) - sum(x from 1 to ll-1)
            # given sum(x from 1 to n) == n(n+1)/2, this works out as
            #
            # = ((rl * (rl+1)) - ((ll-1)*ll)) / 2
            total_repeated += (10**length + 1) * (((rl * (rl+1)) - ((ll-1)*ll)) // 2)

    print(f"{total_repeated=}")



if __name__ == '__main__':
    main()



