# Commutator.py

Python version of [commutator](http://github.com/nbwzx/commutator).

## Overview

Decompose algorithms in commutator notation.

Let $G$ be any group. If $a,b \in G$, then the commutator of $a$ and $b$ is the element $[a,b]=aba^{−1}b^{−1}$. The expression $x\colon a$ denotes the conjugate of $a$ by $x$, defined as $xax^{−1}$. Therefore, $c\colon[a,b]$ means $c a b a^{−1} b^{−1} c^{−1}$.

In this repository, we assume that $G$ is a free group.

In mathematics, the free group $F_{S}$ over a given set $S$ consists of all words that can be built from members of $S$, considering two words to be different unless their equality follows from the group axioms (e.g. $s t=s u u^{-1} t$, but $s \neq t^{-1}$ for $s, t, u \in S$). The members of $S$ are called generators of $F_{S}$, and the number of generators is the rank of the free group. An arbitrary group $G$ is called free if it is isomorphic to $F_{S}$ for some subset $S$ of $G$, that is, if there is a subset $S$ of $G$ such that every element of $G$ can be written in exactly one way as a product of finitely many elements of $S$ and their inverses (disregarding trivial variations such as $s t=s u u^{-1} t$.

It is worth researching since many 3-cycle and 5-cycle algorithms in a Rubik's cube can be decomposed into commutators.

Example 1:

```
Input: s = "R U R' U'"
Output: "[R,U]"
```

Example 2:

```
Input: s = "a b c a' b' c'"
Output: "[a b,c a']"
Explanation: a b + c a' + b' a' + a c' = a b c a' b' c'.
And "[a b,c b]" is also a valid answer.
```

Example 3:

```
Input: s = "D F' R U' R' D' R D U R' F R D' R'"
Output: "D:[F' R U' R',D' R D R']"
And "[D F' R U' R' D',R D R' D']" is also a valid answer.
```

Example 4:

```
Input: s = "R' F' R D' R D R2 F2 R2 D' R' D R' F' R"
Output: "R' F':[R D' R D R2,F2]"
```

Example 5:

```
Input: s = "R U R'"
Output: "Not found."
```

Constraints:

- s consist of only English letters.

## Usage

```
import commutator.commutator as commutator
print(commutator.search("S U' R E' R' U R E R' S'"))
print(commutator.expand("S:[U',R E' R']"))
```

See more examples at `example.py`

Decomposing algorithms in commutator notation with Python using the standard CPython interpreter is not recommended. We recommend using PyPy for performance reasons.

## Contributors

Zixing Wang

## License

MIT License
