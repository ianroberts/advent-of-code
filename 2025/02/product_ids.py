

def ranges(start, end, repeats):
    if len(start) == len(end):
        if len(start) % repeats == 0:
            yield start, end, len(start) // repeats
    else:  # len(start) < len(end)
        if len(start) % repeats == 0:
            yield start, str(10**len(start) - 1), len(start) // repeats
        start = str(10**len(start))
        for i in range(len(start), len(end)):
            if (i+1) % repeats == 0:
                yield str(10**i), str((10**i+1) - 1), (i + 1) // repeats
        if len(end) % repeats == 0:
            yield str(10**(len(end)-1)), end, len(end) // repeats

def all_ranges(start, end):
    for i in range(2, len(end)+1):
        yield from ranges(start, end, i)

def main():
    with open("input", "r") as f:
        data = [tuple(pair.split("-", maxsplit=1)) for pair in f.readline().strip().split(",")]

    total_repeated = 0
    for start, end in data:
        for l, r, length in all_ranges(start, end):
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
            total_repeated += (((rl * (rl+1)) - ((ll-1)*ll)) // 2) * sum(10**(length * i) for i in range(len(l) // length))

            # work out how to deal with the triple-counting of 222222 as 222*2, 22*3 and 2*6
    print(f"{total_repeated=}")



if __name__ == '__main__':
    main()



