# 2025 day 2

## Preprocessing

The reasoning below all applies only to ranges where the start and end points of the range have the same number of digits.  But this is not a problem since any range where the endpoints are different orders of magnitude can be split into adjacent sub-ranges at the power-of-ten boundaries, e.g. the range 12-3456 can be split into 12-99, 100-999 and 1000-3456.  All downstream reasoning assumes this pre-processing, so every range we're dealing with has the same number of digits in both its endpoints.

## Part 1

Working on part 1 of this problem I realised early on that there's a nice mathematical way to approach it that avoids having to enumerate every possible number in every range and check them all for duplicates.  The key insight was that given any range where both ends have the same (even) number $d$ of digits you can split the two endpoints into two half-length digit strings and treat those as separate numbers.  The reasoning is as follows:

Given range endpoints $S$ and $E$ with $d$ digits each, we can break them into two $d/2 = c$-digit chunks as

```math
\begin{align}
S = 10^c . S_2 + S_1 \\
E = 10^c . E_2 + E_1
\end{align}
```

(i.e. $X_2$ is the left half and $X_1$ is the right half of each endpoint - the numbering will become clearer later).  Now the repeats in this sequence will be numbers where both halves have the same value $m$ for all $m$ between the following values (inclusive):

- $R_S = S_2+1$, if $S_2 < S_1$, or $R_S = S_2$ otherwise
- $R_E = E_2-1$, if $E_2 > E_1$, or $R_E = E_2$ otherwise

As a concrete example, if the range endpoints are 456345 - 500478, then the first repeat in that range will be 456456 (since 456 > 345, and the last repeat will be 499499 (since 500 > 478, so 500500 would be out of range).  If $R_S > R_E$ then there are no possible repeats in this range; otherwise, the sum of all repeats in the range will be

$$\sum_{m=R_S}^{R_E} \left(m . (10^c+1)\right)$$

The $10^c+1$ is a "repetition factor" which depends on the number of digits in each chunk - it essentially puts a 1 in each of the halves e.g. 456456 is 456 multiplied by (00)1001.  Now a bit of algebra:

```math
\begin{align}
\sum_{m=R_S}^{R_E} \left(m . (10^c+1)\right) & = & (10^c+1) \left[\sum_{m=R_S}^{R_E} m \right] \\
                                             & = & (10^c+1) \left[\left(\sum_{m=1}^{R_E} m\right) - \left(\sum_{m=1}^{R_S-1} m\right) \right] \\
                                             & = & (10^c+1) \left[\frac{R_E (R_E+1) - (R_S-1) R_S}{2}\right] \\
\end{align}
```

using the fact that $\sum_{k=1}^{n}k = n(n+1)/2$.

## Part 2

The same logic generalises for part 2 to _any_ even split of any $d$-digit endpoints $S$ and $E$ into $k$ chunks of $d/k = c$ digits each.  In this case each endpoint is made up of $k$ chunks named as $S_k$, $S_{k-1}$, ... $S_1$ and $E_k$, $E_{k-1}$, ... $E_1$, i.e. the numeric values are

```math
\begin{align}
S & = & \sum_{i=1}^{k} \left( 10^{i-1} . S_i \right) \\
E & = & \sum_{i=1}^{k} \left( 10^{i-1} . E_i \right)
\end{align}
```

(this is why I numbered them from right to left).  The logic for whether $R_S = S_k$ or $S_k+1$ and whether $R_E = E_k$ or $E_k-1$ is slightly more complicated, now we need to look for the _leftmost_ chunk $S_i$ or $E_j$ that is _not equal_ to the first chunk $S_k$ or $E_k$, and adjust the start/end based on which of these is larger.  For example if we're splitting a 9-digit number into 3 chunks of 3, then the first valid repeat after a start endpoint of 456456765 would be 457457457 since 456 < 765, but the first repeat after 456456321 would be 456456456.

The "repetition factor" this time is $\sum_{i=1}^{k} 10^{(i-1)c}$ - again this effectively puts a 1 in each chunk position.  E.g. 456456456 is 456 multiplied by (00)1001001.  The rest of the algebra is exactly the same:

```math
\begin{align}
\sum_{m=R_S}^{R_E} \left(m . \sum_{i=1}^{k} 10^{(i-1)c}\right) & = & \left(\sum_{i=1}^{k} 10^{(i-1)c}\right) \left(\sum_{m=R_S}^{R_E} m \right) \\
                                & = & \left(\sum_{i=1}^{k} 10^{(i-1)c}\right) \left[\left(\sum_{m=1}^{R_E} m\right) - \left(\sum_{m=1}^{R_S-1} m\right) \right] \\
                                & = & \left(\sum_{i=1}^{k} 10^{(i-1)c}\right) \left[\frac{R_E (R_E+1) - (R_S-1) R_S}{2}\right] \\
\end{align}
```

We now have a closed-form expression for all the $k$-chunk splits of every range, the difficulty lies in working out which values of $k$ we need to split for each digit length $d$, and how to make sure we count each "invalid ID" exactly once, with none missed or duplicated.

### Prime factors, and the inclusion-exclusion principle

The trick is to consider the prime factors of $d$.  To be able to split a $d$-digit number evenly into $k$ chunks, $k$ must be some product of one or more of the prime factors of $d$.  Any $k$ with repeated factors can be ignored, since any repeating pattern of digits arising from a split into $k \times j$ chunks must necessarily also be a repeating pattern that could arise from $k$ chunks (e.g. for twelve digits, 121212121212 is a repeating pattern in 6 chunks of 2 digits each, but it's also a repeating pattern in 3 chunks of 4 and in 2 chunks of 6).  So if $d$ has a set of _distinct_ prime factors $P = \lbrace p_1, p_2, \ldots p_j \rbrace$ then what we need is the _union_ of the set of repeats arising from $p_1$ chunks, and the set of repeats arising from $p_2$ chunks, etc. up to $p_j$.  The way to get all of these without repeats is the inclusion-exclusion principle:

```math
\begin{aligned}
\left| A \cup B \right| &= \left| A \right| + \left| B \right| - \left| A \cap B \right| \\
\left| A \cup B \cup C \right| &= \left| A \right| + \left| B \right| + \left| C \right| - \left| A \cap B \right| - \left| A \cap C \right| - \left| B \cap C \right| + \left| A \cap B \cap C \right| \\
                 & \vdots
\end{aligned}
```

Add the individual sets, subtract the 2-set intersections, add back in the 3-set intersections, etc.  In general we want to consider all possible combinations of the distinct prime factors (i.e. all non-empty subsets $C \subseteq P$), calculate the total repeats when splitting into $\prod C$ chunks, then _add_ this to the running total if $|C|$ is odd, or _subtract_ it from the total if $|C|$ is even.

## Performance

[Brute-force version](store_values.py)

This approach is more or less linear in the total number of points in all the ranges (on the order of $10^{10}$ for the given test data).

```
Part 1: total_repeated=30323879646
Time: 0.2612517918460071
Part 2: total_repeated=43872163557
Time: 0.20210270886309445
```

[Mathematical version](product_ids.py)

Here the calculation for each $k$ split of each range is effectively `O(1)`, and the number of calculations we have to do will be the number of ranges times $2^p-1$ where $p$ is the number of prime factors of the length-in-digits of the range endpoint.  Concretely, in the actual test data the largest range endpoint is 10 digits, so the all the possible lengths have either 1 or 2 prime factors ($6 = 2 \times 3$, $10 = 2 \times 5$, everything else is either prime - $2, 3, 5, 7$ - or a power of a single factor - $4 = 2 \times 2$, $8 = 2 \times 2 \times 2$, and $9 = 3 \times 3$), so it'll be 1 or 3 calculations per range.

```
Part 1: total_repeated=30323879646
Time: 7.545808330178261e-05
Part 2: total_repeated=43872163557
Time: 0.00018754089251160622
```

(~1000x faster).