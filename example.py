import commutator.commutator as commutator
from typing import List
import time

res1: List[str] = []
res2 = ""

t0 = time.time()
print("The commutator of a b4 c b a' b2' c' b3' in different orders.")
for orderInput in range(11):
    res2 = commutator.search("a b4 c b a' b2' c' b3'", orderInput)[0]
    print("order = ", orderInput, ", commutator = ", res2)
t1 = time.time()
print("Test 1:", t1 - t0, "seconds")

t0 = time.time()
print("The expand of [a b,b3 c b2] in different orders.")
for orderInput in range(11):
    res2 = commutator.expand("[a b,b3 c b2]", orderInput)
    print("order = ", orderInput, ", expand = ", res2)
t1 = time.time()
print("Test 2:", t1 - t0, "seconds")

t0 = time.time()
print("Single commutator:")
print("The commutator of U' R U R2 D' R2 U' R' U R2 D R2 in order 4.")
res1 = commutator.search("U' R U R2 D' R2 U' R' U R2 D R2",
                         orderInput=4, outerBracketInput=True, limit=3)
print(res1)
t1 = time.time()
print("Test 3:", t1 - t0, "seconds")

t0 = time.time()
print("Combination of commutators:")
print("The combination of commutators of R U' S U2 S R' S2 R U' R' in order 4.")
res1 = commutator.search("R U' S U2 S R' S2 R U' R'",
                         orderInput=4, outerBracketInput=True, limit=3)
print(res1)
t1 = time.time()
print("Test 4:", t1 - t0, "seconds")
