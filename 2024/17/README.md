# AoC 2024 day 17

([link](https://adventofcode.com/2024/day/17))

Part 1 was easy - just build an interpreter for the bytecode language and run the program.

Part 2 we need to dig into a bit of disassembly.  My input program is equivalent to the following "assembly language", with two magic constants `k1` and `k2` found at program indices 3 and 7 respectively:

```
0: bst 4   b := a % 8 (lowest three bits of a)
1: bxl k1  b := b ^ k1
2: cdv 5   c := a >> b
3: bxl k2  b := b ^ k2
4: bxc 3   b := b ^ c
5: out 5   output lowest three bits of b
6: adv 3   a := a >> 3
7: jnz 0   if a != 0: goto 0
```

Each time around the loop the program will output one number, and end by right shifting `a` by three bits.  So we can consider each output number in isolation and ask "if we want to output the number N, what constraints does that place on the value of `a` at the start of this iteration?"

Working backwards through the program, if we want to output an `N` at line 5 then the three least significant bits of `b^c` at line 4 must equal `N`.  There are eight possibilities for `b`, and each of those has a corresponding `c` (whose three LSBs must equal `N ^ b`) that will produce the correct result.

Where did these values come from?

- `b` is the three LSBs of `a ^ k1 ^ k2`
- `N ^ b` is the three LSBs of `a >> ((a & 7) ^ k1)`.

Therefore ultimately we're going to end up, for each `N`, with a set of up to 8 different "patterns" for different `b` that constrain some (but not all) of the lowest 10 bits of `a`

`b = (a ^ k1 ^ k2) & 7` implies that `a & 7 = b ^ k1 ^ k2` - the three LSBs of `a` must be `b ^ k1 ^ k2`.  We can then reason as follows:

- `(N ^ b) & 7 = (a >> ((a & 7) ^ k1)) & 7`
- `(N ^ b) & 7 = (a >> ((b ^ k1 ^ k2) ^ k1)) & 7`
- `(N ^ b) & 7 = (a >> (b ^ k2)) & 7`

so bits `b ^ k2` to `(b ^ k2) + 2` (counting from the right) of `a` must equal `N ^ b`.

This is all preamble to explain my approach to part 2: if we want the program to output itself, then we need to find the smallest input number `a` that satisfies:

- at least one of the possible base patterns that can generate the program's first digit, and
- at least one of the base patterns that can generate the second digit, shifted left by three bits, and
- at least one of the base patterns that can generate the third digit, shifted left by six bits
- etc.

At each step we attempt to _merge_ each of the new patterns for this step with each of the existing patterns that could constrain the sequence up to this point.  Two patterns are compatible if all the bits that are constrained by both patterns are the same in both, and the merged pattern is the union of the constrained bits from both parent patterns.  Incompatible combinations are discarded.

Once all the constraints from all steps are merged, we are left with a set of patterns that would generate the program as its own output, the final answer is the smallest number that satisfies at least one of these patterns.