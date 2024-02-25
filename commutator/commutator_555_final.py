"""
Commutator (https://github.com/nbwzx/commutator.py)
Copyright (c) 2022-2024 Zixing Wang <zixingwang.cn@gmail.com>
Licensed under MIT (https://github.com/nbwzx/commutator.py/blob/main/LICENSE)
"""
from typing import Dict, List
import commutator.commutator as commutator
import commutator.commutator_555 as commutator_555

commuteInit = {
    'U': {'class': 1, 'priority': 1},
    'u': {'class': 1, 'priority': 2},
    'e': {'class': 1, 'priority': 3},
    'd': {'class': 1, 'priority': 4},
    'D': {'class': 1, 'priority': 5},
    'R': {'class': 2, 'priority': 1},
    'r': {'class': 2, 'priority': 2},
    'm': {'class': 2, 'priority': 3},
    'l': {'class': 2, 'priority': 4},
    'L': {'class': 2, 'priority': 5},
    'F': {'class': 3, 'priority': 1},
    'f': {'class': 3, 'priority': 2},
    's': {'class': 3, 'priority': 3},
    'b': {'class': 3, 'priority': 4},
    'B': {'class': 3, 'priority': 5}
}


initialReplaceInit = {
    "y2": "U2 u2 e2 d2 D2",
    "x2": "R2 r2 m2 l2 L2",
    "z2": "F2 f2 s2 b2 B2",
    "4Uw2": "U2 u2 e2 d2",
    "4Lw2": "r2 m2 l2 L2",
    "4Fw2": "F2 f2 s2 b2",
    "4Rw2": "R2 r2 m2 l2",
    "4Dw2": "u2 e2 d2 D2",
    "4Bw2": "f2 s2 b2 B2",
    "3Uw2": "U2 u2 e2",
    "3Lw2": "m2 l2 L2",
    "3Fw2": "F2 f2 s2",
    "3Rw2": "R2 r2 m2",
    "3Dw2": "e2 d2 D2",
    "3Bw2": "s2 b2 B2",
    "Uw2": "U2 u2",
    "Lw2": "l2 L2",
    "Fw2": "F2 f2",
    "Rw2": "R2 r2",
    "Dw2": "d2 D2",
    "Bw2": "b2 B2",
    "x'": "R' r' m l L",
    "y'": "U' u' e d D",
    "z'": "F' f' s' b B",
    "4Uw'": "U' u' e d",
    "4Lw'": "r m' l' L'",
    "4Fw'": "F' f' s' b",
    "4Rw'": "R' r' m l",
    "4Dw'": "u e' d' D'",
    "4Bw'": "f s b' B'",
    "3Uw'": "U' u' e",
    "3Lw'": "m' l' L'",
    "3Fw'": "F' f' s'",
    "3Rw'": "R' r' m",
    "3Dw'": "e' d' D'",
    "3Bw'": "s b' B'",
    "Uw'": "U' u'",
    "Lw'": "l' L'",
    "Fw'": "F' f'",
    "Rw'": "R' r'",
    "Dw'": "d' D'",
    "Bw'": "b' B'",
    "x": "R r m' l' L'",
    "y": "U u e' d' D'",
    "z": "F f s b' B'",
    "4Uw": "U u e' d'",
    "4Lw": "r' m l L",
    "4Fw": "F f s b'",
    "4Rw": "R r m' l'",
    "4Dw": "u' e d D",
    "4Bw": "f' s' b B",
    "3Uw": "U u e'",
    "3Lw": "m l L",
    "3Fw": "F f s",
    "3Rw": "R r m'",
    "3Dw": "e d D",
    "3Bw": "s' b B",
    "Uw": "U u",
    "Lw": "l L",
    "Fw": "F f",
    "Rw": "R r",
    "Dw": "d D",
    "Bw": "b B",
    "E2": "u2 e2 d2",
    "M2": "r2 m2 l2",
    "S2": "f2 s2 b2",
    "E'": "u e' d'",
    "M'": "r m' l'",
    "S'": "f' s' b",
    "E": "u' e d",
    "M": "r' m l",
    "S": "f s b'",
}

finalReplaceInit: Dict[str, str] = {}


def search(algorithm: str) -> List[str]:
    return commutator.search(algorithm=algorithm, initialReplaceInput=initialReplaceInit, finalReplaceInput=finalReplaceInit, commuteInput=commuteInit)


def expand(algorithm: str) -> str:
    return commutator.expand(algorithm=algorithm, initialReplaceInput=initialReplaceInit, finalReplaceInput=finalReplaceInit, commuteInput=commuteInit)


# TODO: clean and generalize this
def finalReplaceAlg(alg: str) -> str:
    alg = commutator_555.expand(alg)
    new_alg = ""
    while alg != new_alg:
        if new_alg != "":
            alg = new_alg
        arr = alg.split(" ")
        i = 0
        while i < len(arr) - 1:
            expanded = expand(arr[i] + " " + arr[i + 1])
            if expanded.count(" ") == 0:
                arr[i] = expanded
                arr.pop(i + 1)
                i -= 1
            else:
                for j in initialReplaceInit:
                    if expanded == initialReplaceInit[j]:
                        arr[i] = j
                        arr.pop(i + 1)
                        i -= 1
                        break
            i += 1
        new_alg = " ".join(arr)
        new_alg = commutator_555.expand(new_alg)
    alg = new_alg
    new_alg = ""
    while alg != new_alg:
        if new_alg != "":
            alg = new_alg
        arr = alg.split(" ")
        i = 0
        while i < len(arr) - 2:
            expanded = expand(arr[i] + " " + arr[i + 1] + " " + arr[i + 2])
            if expanded.count(" ") == 0:
                arr[i] = expanded
                arr.pop(i + 2)
                arr.pop(i + 1)
                i -= 1
            else:
                for j in initialReplaceInit:
                    if expanded == initialReplaceInit[j]:
                        arr[i] = j
                        arr.pop(i + 2)
                        arr.pop(i + 1)
                        i -= 1
                        break
            i += 1
        new_alg = " ".join(arr)
        new_alg = commutator_555.expand(new_alg)
    return new_alg


# TODO: clean and generalize this
def finalReplaceCommutator(alg: str) -> str:
    if "[" not in alg or "]" not in alg or "," not in alg:
        return alg
    if ":" in alg:
        part0 = alg.split(":")[0]
        part0 = finalReplaceAlg(part0)
        part1 = alg.split("[")[1].split(",")[0]
        part1 = finalReplaceAlg(part1)
        part2 = alg.split(",")[1].split("]")[0]
        part2 = finalReplaceAlg(part2)
        alg = part0 + ":[" + part1 + "," + part2 + "]"
    else:
        part1 = alg.split("[")[1].split(",")[0]
        part1 = finalReplaceAlg(part1)
        part2 = alg.split(",")[1].split("]")[0]
        part2 = finalReplaceAlg(part2)
        alg = "[" + part1 + "," + part2 + "]"
    return alg
