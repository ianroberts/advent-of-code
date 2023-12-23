# Day 20 part 2

This is less of a programming problem and more a puzzle about analyzing the structure of the particular graph you've been given as your puzzle input.

![My graph](graph.drawio.svg)

Each of the four sections is a cascade of flipflops that essentially act as a binary counter with the least significant bit at the top and the most significant at the bottom - the initial state is all zeros and each press of the button counts up by one:

```
   1 000000000001
   2 000000000010
   3 000000000011
   4 000000000100
   5 000000000101
   6 000000000110
   7 000000000111
   8 000000001000
   9 000000001001
  10 000000001010
  11 000000001011
  12 000000001100
  13 000000001101
  14 000000001110
  15 000000001111
  16 000000010000
```

The links down from specific flipflop bits to the output NAND mean that the output NAND will generate a low pulse when all those bits are 1 in the binary representation of the counter value.  The links _up_ from the output NAND back to the other flipflops mean that as soon as the counter _first_ reaches that target value it will immediately reset to zero, ready to start counting up again.  Consider this four bit example:


| Bit   | 3 | 2  | 1  | 0   |
|-------|---|----|----|-----|
| State | 1 | 0  | 0  | 1   |
| Links | ↓ | ←↑ | ←↑ | ←↕︎ |

Up and down links are from/to the output NAND, left links are to the next bit. The counter has just ticked over to the value 9 (1001 binary), so the output NAND now sees all 1s and it sends a low pulse to the output and also to all of its up-links (to the least significant bit, plus the other bits that are zero at the target value).

- The low pulse sent up to bit 0 flips this to 0 and sends a low _left_ to bit 1
- The low pulse sent _up_ to bit 1 flips this to 1, but it flips back to 0 on receipt of the low from bit 0 and sends a low _left_ to bit 2
- The low pulse sent _up_ to bit 2 flips bit 2 to a 1, but it flips back to 0 on receipt of the low from bit 1 and sends another low _left_ to bit 3
- Bit 3 didn't get a low _up_ from the output NAND, so the low from bit 2 flips bit 3 to 0 and sends a low to the output NAND
- The output NAND sends high pulses to all the flipflops, which are ignored

So the new steady state is all zeros ready for the next button push.

## Answer to the puzzle

Therefore, from the graph structure we can see that the final output NAND `zh` will see a high pulse on each of its inputs as follows:

- from chain 1: every 111010110001 binary = 3761 presses
- from chain 2: every 111011000011 binary = 3779 presses
- from chain 3: every 111010110111 binary = 3767 presses
- from chain 4: every 111100101001 binary = 3881 presses

Therefore the final `rx` output will see a low after the lowest common multiple of these numbers, which is **207787533680413**.