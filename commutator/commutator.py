"""
Commutator (https://github.com/nbwzx/commutator.py)
Copyright (c) 2022-2024 Zixing Wang <zixingwang.cn@gmail.com>
Licensed under MIT (https://github.com/nbwzx/commutator.py/blob/main/LICENSE)
"""
import re
from typing import Dict, List

MAX_INT = 4294967295
orderInit = 4
outerBracketInit = False
abMaxScoreInit: float = 2.5
abMinScoreInit: float = 5
addScoreInit: float = 1
maxDepthInit = 0
limitInit = 0
fastInit = False

commuteInit = {
    'U': {'class': 1, 'priority': 1},
    'E': {'class': 1, 'priority': 2},
    'D': {'class': 1, 'priority': 3},
    'R': {'class': 2, 'priority': 1},
    'M': {'class': 2, 'priority': 2},
    'L': {'class': 2, 'priority': 3},
    'F': {'class': 3, 'priority': 1},
    'S': {'class': 3, 'priority': 2},
    'B': {'class': 3, 'priority': 3}
}


initialReplaceInit = {
    "Rw2": "r2",
    "Rw'": "r'",
    "Rw": "r",
    "Lw2": "l2",
    "Lw'": "l'",
    "Lw": "l",
    "Fw2": "f2",
    "Fw'": "f'",
    "Fw": "f",
    "Bw2": "b2",
    "Bw'": "b'",
    "Bw": "b",
    "Uw2": "u2",
    "Uw'": "u'",
    "Uw": "u",
    "Dw2": "d2",
    "Dw'": "d'",
    "Dw": "d",
    "r2": "R2 M2",
    "r'": "R' M",
    "r": "R M'",
    "l2": "M2 L2",
    "l'": "M' L'",
    "l": "M L",
    "f2": "F2 S2",
    "f'": "F' S'",
    "f": "F S",
    "b2": "S2 B2",
    "b'": "S B'",
    "b": "S' B",
    "u2": "U2 E2",
    "u'": "U' E",
    "u": "U E'",
    "d2": "E2 D2",
    "d'": "E' D'",
    "d": "E D"
}

finalReplaceInit = {
    "R2 M2": "r2",
    "R' M": "r'",
    "R M'": "r",
    "M2 L2": "l2",
    "M' L'": "l'",
    "M L": "l",
    "F2 S2": "f2",
    "F' S'": "f'",
    "F S": "f",
    "S2 B2": "b2",
    "S B'": "b'",
    "S' B": "b",
    "U2 E2": "u2",
    "U' E": "u'",
    "U E'": "u",
    "E2 D2": "d2",
    "E' D'": "d'",
    "E D": "d",
    "M2 R2": "r2",
    "M R'": "r'",
    "M' R": "r",
    "L2 M2": "l2",
    "L' M'": "l'",
    "L M": "l",
    "S2 F2": "f2",
    "S' F'": "f'",
    "S F": "f",
    "B2 S2": "b2",
    "B' S": "b'",
    "B S'": "b",
    "E2 U2": "u2",
    "E U'": "u'",
    "E' U": "u",
    "D2 E2": "d2",
    "D' E'": "d'",
    "D E": "d",
    "R M2": "r M'",
    "R' M2": "r' M",
    "M2 R": "r M'",
    "M2 R'": "r' M",
    "U2 E": "U' u'",
    "U2 E'": "U u",
    "E U2": "U' u'",
    "E' U2": "U u",
    "U E2": "u E'",
    "U' E2": "u' E",
    "E2 U": "u E'",
    "E2 U'": "u' E",
    "r L'": "x",
    "r' L": "x'",
    "r2 L2": "x2"
}


class Move(object):
    def __init__(self, base, amount):
        self.base = base
        self.amount = amount


result: List[str] = []
order = orderInit
minAmount = orderInit // 2 + 1 - orderInit
maxAmount = orderInit // 2
maxAlgAmount = 0
isOrderZero = False
outerBracket = outerBracketInit
abMaxScore = abMaxScoreInit
abMinScore = abMinScoreInit
addScore = addScoreInit
fast = False
commute = commuteInit
initialReplace = initialReplaceInit
finalReplace = finalReplaceInit


def expand(algorithm: str, orderInput: int = orderInit, initialReplaceInput: Dict[str, str] = initialReplaceInit, finalReplaceInput: Dict[str, str] = finalReplaceInit, commuteInput: Dict[str, Dict[str, int]] = commuteInit, isInverse: bool = False) -> str:
    global order
    global initialReplace
    global finalReplace
    global commute
    global isOrderZero
    global minAmount
    global maxAmount
    order = orderInput
    initialReplace = initialReplaceInput
    finalReplace = finalReplaceInput
    commute = commuteInput
    algorithm = re.sub(r'\s', ' ', algorithm)
    algorithm = algorithm.replace(';', ":")
    algorithm = algorithm.replace('‘', "'")
    algorithm = algorithm.replace('’', "'")
    algorithm = algorithm.replace('（', '')
    algorithm = algorithm.replace('）', '')
    algorithm = algorithm.replace('{', '')
    algorithm = algorithm.replace('}', '')
    algorithm = algorithm.replace(' ', '')
    algorithm = algorithm.replace('!', '')
    algorithm = algorithm.replace('！', '')
    algorithm = algorithm.replace('×', '*')
    algorithm = algorithm.replace('*2', '2')
    new_algorithm = algorithm
    # TODO: clean and generalize this
    for i in range(len(algorithm) - 1, 1, -1):
        if algorithm[i] == "2" and algorithm[i - 1] == ")":
            j = i - 1
            while algorithm[j] != "(" and j >= 0:
                j -= 1
            if j >= 0:
                new_algorithm = algorithm[0:j] + algorithm[j + 1:i - 1] + \
                    algorithm[j + 1:i - 1] + algorithm[i + 1:len(algorithm)]
                break
    algorithm = new_algorithm
    algorithm = algorithm.replace('(', '')
    algorithm = algorithm.replace(')', '')
    algorithm = algorithm.replace('【', '[')
    algorithm = algorithm.replace('】', ']')
    algorithm = algorithm.replace('：', ':')
    algorithm = algorithm.replace('，', ',')
    algorithm = algorithm.replace(': ', ':')
    algorithm = algorithm.replace(', ', ',')
    algorithm = algorithm.replace('[ ', '[')
    algorithm = algorithm.replace('] ', ']')
    algorithm = algorithm.replace(' :', ':')
    algorithm = algorithm.replace(' ,', ',')
    algorithm = algorithm.replace(' [', '[')
    algorithm = algorithm.replace(' ]', ']')
    algorithm = '[' + algorithm.replace('+', ']+[') + ']'
    algorithm = algorithm.replace('][', ']+[')
    if order == 0:
        isOrderZero = True
        order = MAX_INT
    else:
        isOrderZero = False
    minAmount = (order // 2) + 1 - order
    maxAmount = order // 2
    rpnStack = rpn(initStack(algorithm))
    if len(rpnStack) == 0:
        return 'Empty input.'
    if rpnStack[0] == 'Lack left parenthesis.' or rpnStack[0] == 'Lack right parenthesis.':
        return rpnStack[0]
    calcTemp = calc(rpnStack)
    if calcTemp == '':
        return 'Empty input.'
    if isInverse:
        expandOutput = arrayToStr(invert(algToArray(calcTemp)))
    else:
        expandOutput = arrayToStr(algToArray(calcTemp))
    if expandOutput == '':
        return 'Empty input.'
    return expandOutput


def isOperator(sign: str) -> bool:
    operatorString = "+:,/[]"
    return sign in operatorString


def initStack(algorithm: str) -> List[str]:
    stack = [algorithm[0]]
    for i in range(1, len(algorithm)):
        if isOperator(algorithm[i]) or isOperator(stack[-1]):
            stack.append(algorithm[i])
        else:
            stack[-1] += algorithm[i]
    return stack


def operatorLevel(operator: str) -> int:
    if operator == ":":
        return 0
    elif operator == ",":
        return 1
    elif operator == "/":
        return 2
    elif operator == "+":
        return 3
    elif operator == "[":
        return 4
    elif operator == "]":
        return 5
    else:
        return -1


def rpn(stackInput: List[str]) -> List[str]:
    stackOutput: List[str] = []
    operatorStack: List[str] = []
    isMatch = False
    operatorStackPop = ""
    while stackInput:
        sign = stackInput.pop(0)
        if not isOperator(sign):
            stackOutput.append(sign)
        elif sign == "]":
            isMatch = False
            while operatorStack:
                operatorStackPop = operatorStack.pop()
                if operatorStackPop == "[":
                    isMatch = True
                    break
                else:
                    stackOutput.append(operatorStackPop)
            if not isMatch:
                return ["Lack left parenthesis."]
        else:
            while operatorStack and operatorStack[-1] != "[" and operatorLevel(sign) <= operatorLevel(operatorStack[-1]):
                stackOutput.append(operatorStack.pop())
            operatorStack.append(sign)
    while operatorStack:
        operatorStackPop = operatorStack.pop()
        if operatorStackPop == "[":
            return ["Lack right parenthesis."]
        stackOutput.append(operatorStackPop)
    return stackOutput


def calc(stack: List[str]) -> str:
    calc_output: List[str] = []
    while len(stack) > 0:
        sign = stack.pop(0)
        if isOperator(sign):
            if len(calc_output) >= 2:
                calc_pop2 = calc_output.pop()
                calc_pop1 = calc_output.pop()
                calc_output.append(calcTwo(calc_pop1, calc_pop2, sign))
            else:
                return ""
        else:
            calc_output.append(sign)
    return calc_output[0] if len(calc_output) > 0 else ""


def calcTwo(algorithm1: str, algorithm2: str, sign: str) -> str:
    array1, array2 = [], []
    array1 = algToArray(algorithm1)
    array2 = algToArray(algorithm2)
    if sign == "+":
        return arrayToStr(array1 + array2)
    elif sign == ":":
        return arrayToStr(array1 + array2 + invert(array1))
    elif sign == ",":
        return arrayToStr(array1 + array2 + invert(array1) + invert(array2))
    elif sign == "/":
        return arrayToStr(array1 + array2 + invert(array1) * 2 + invert(array2) + array1)
    else:
        return arrayToStr(array1 + array2)


def score(algorithm: str) -> float:
    alg = algorithm
    alg = f"[{alg.replace('+', ']+[')}]"
    alg = alg.replace('][', ']+[')
    rpnStack = rpn(initStack(alg))
    scoreOutput: List[str] = []
    while len(rpnStack) > 0:
        sign = rpnStack.pop(0)
        if isOperator(sign):
            scorePop2 = scoreOutput.pop()
            scorePop1 = scoreOutput.pop()
            score1 = float(scorePop1) if is_number(scorePop1) else len(
                scorePop1.split())
            score2 = float(scorePop2) if is_number(scorePop2) else len(
                scorePop2.split())
            scoreOutput.append(str(scoreTwo(score1, score2, sign)))
        else:
            scoreOutput.append(sign)
    return float(scoreOutput[0])


def is_number(strInput: str) -> bool:
    try:
        if strInput == 'NaN':
            return False
        float(strInput)
        return True
    except ValueError:
        return False


def scoreTwo(score1: float, score2: float, sign: str) -> float:
    if sign == "+":
        return score1 + score2 + addScore
    elif sign == ":":
        return score1 + score2
    elif sign == ",":
        return abMaxScore * max(score1, score2) + abMinScore * min(score1, score2)
    else:
        return MAX_INT


def search(algorithm: str, orderInput: int = orderInit, outerBracketInput: bool = outerBracketInit, abMaxScoreInput: float = abMaxScoreInit, abMinScoreInput: float = abMinScoreInit, addScoreInput: float = addScoreInit, initialReplaceInput: Dict[str, str] = initialReplaceInit, finalReplaceInput: Dict[str, str] = finalReplaceInit, commuteInput: Dict[str, Dict[str, int]] = commuteInit, fastInput: bool = fastInit, maxDepth: int = maxDepthInit, limit: int = limitInit) -> List[str]:
    global order
    global outerBracket
    global abMaxScore
    global abMinScore
    global addScore
    global initialReplace
    global finalReplace
    global commute
    global fast
    global result
    global isOrderZero
    global minAmount
    global maxAmount
    order = orderInput
    outerBracket = outerBracketInput
    abMaxScore = abMaxScoreInput
    abMinScore = abMinScoreInput
    addScore = addScoreInput
    initialReplace = initialReplaceInput
    finalReplace = finalReplaceInput
    commute = commuteInput
    fast = fastInput
    result = []
    if algorithm == "":
        return ["Empty input."]
    arr = algToArray(algorithm)
    if order == 0:
        isOrderZero = True
        order = 2 * (maxAlgAmount + 2)
    else:
        isOrderZero = False
    # Examples:
    # • order 4 → min -1 (e.g. cube)
    # • order 5 → min -2 (e.g. Megaminx)
    # • order 3 → min -1 (e.g. Pyraminx)
    minAmount = (order // 2) + 1 - order
    maxAmount = order // 2
    arr = simplify(arr)
    arrLen = len(arr)
    if arrLen == 0:
        return ["Empty input."]
    for i in range(arrLen):
        amountCount = 0
        for j in range(arrLen):
            if arr[i].base == arr[j].base:
                amountCount = amountCount + arr[j].amount
        if amountCount % order != 0:
            return ["Not found."]
    commuteCount = 0
    commuteIndex = []
    for i in range(arrLen - 1):
        if isSameClass(arr[i], arr[i + 1]):
            commuteIndex.append(i)
            commuteCount += 1
    commuteTotal = 2 ** commuteCount
    commutatorOutput = ["Not found."]
    isFind = False
    if maxDepth == 0:
        searchDepth = (arrLen - 1) // 3
    else:
        searchDepth = maxDepth
    for depth in range(1, searchDepth + 1):
        for i in range(commuteTotal):
            commuteArr = arr.copy()
            for j in range(commuteCount):
                if i & (1 << j):
                    commuteArr[commuteIndex[j]], commuteArr[commuteIndex[j] +
                                                            1] = commuteArr[commuteIndex[j] + 1], commuteArr[commuteIndex[j]]
            commutatorOutput = commutatorMain(commuteArr, depth, depth)
            if commutatorOutput[0] != "Not found.":
                isFind = True
            if fast and isFind:
                return result
        if isFind and (depth == maxDepth or maxDepth == 0):
            result.sort(key=lambda alg: score(alg))
            if limit == 0:
                return result
            return result[:limit]
    return ["Not found."]


def commutatorPre(array: List[Move], depth: int, maxSubDepth: int) -> List[str]:
    commuteCount = 0
    commuteIndex = []
    for i in range(len(array) - 1):
        if isSameClass(array[i], array[i + 1]):
            commuteIndex.append(i)
            commuteCount += 1
    commuteTotal = 2 ** commuteCount
    commutatorResult = ["Not found."]
    for i in range(commuteTotal):
        commuteArr = array.copy()
        for j in range(commuteCount):
            if i & (1 << j):
                commuteArr[commuteIndex[j]], commuteArr[commuteIndex[j] +
                                                        1] = commuteArr[commuteIndex[j] + 1], commuteArr[commuteIndex[j]]
        commutatorResult = commutatorMain(commuteArr, depth, maxSubDepth)
        if commutatorResult[0] != "Not found.":
            return commutatorResult
    return ["Not found."]


def commutatorMain(array: List[Move], depth: int, maxSubDepth: int) -> List[str]:
    arr = simplify(array)
    commutatorOutput = ""
    arrBak = arr.copy()
    arrLen = len(arr)
    if len(arr) < 3 * depth + 1:
        return ["Not found."]
    for d in range(0, (arrLen + len(arr) + 1) // 2):
        if d >= (arrLen + len(arr) + 1) // 2:
            continue
        for drKey in range(1, order):
            # 1, -1, 2, -2...
            dr = ((drKey % 2) * 2 - 1) * ((drKey + 1) // 2)
            if d == 0:
                if drKey > 1:
                    break
            else:
                if abs(dr) > abs(arrBak[d - 1].amount):
                    break
                if order % 2 == 1 or arrBak[d - 1].amount != order // 2:
                    if (arrBak[d - 1].amount < 0 and dr > 0) or (arrBak[d - 1].amount > 0 and dr < 0):
                        continue
            arr = displace(arrBak, d, dr)
            for i in range(1, len(arr) // 2):
                if depth == 1:
                    minj = max(1, (len(arr) + 1) // 2 - i)
                else:
                    minj = 1
                for j in range(minj, len(arr) // 2):
                    part1x, part2x = [], []
                    commuteAdd1: List[List[Move]] = []
                    commuteAdd2: List[List[Move]] = []
                    if arr[i - 1].base == arr[i + j - 1].base:
                        # For [a bx,by c bz]
                        for ir in range(minAmount, maxAmount + 1):
                            if ir == 0:
                                continue
                            jr = normalize(arr[i + j - 1].amount + ir)
                            part1x = simplify(repeatEnd(arr[:i], ir))
                            commuteAdd1.append(part1x)
                            part2x = simplify(
                                invert(part1x) + repeatEnd(arr[:i + j], jr))
                            commuteAdd2.append(part2x)
                    else:
                        if depth == 1 and arr[i].base != arr[-1].base:
                            continue
                        part1x = simplify(arr[:i])
                        commuteAdd1.append(part1x)
                        part2x = simplify(arr[i:i + j])
                        commuteAdd2.append(part2x)
                        commuteCase = []
                        if isSameClass(arr[i - 1], arr[i + j - 1]):
                            # For L a R b L' a' R' b' = [L a R,b L' R]
                            commuteAdd1.append(part1x)
                            commuteCase = simplify(part2x + [arr[i - 1]])
                            commuteAdd2.append(commuteCase)
                            # For L a R L b R L2' a' R2' b' = [L a R L,b R2 L']
                            if i >= 2:
                                if isSameClass(arr[i - 1], arr[i - 2]):
                                    commuteAdd1.append(part1x)
                                    commuteCase = simplify(
                                        part2x + arr[i - 2:i])
                                    commuteAdd2.append(commuteCase)
                        if isSameClass(arr[i], arr[i + j]):
                            # For a R b L a' R' b' L' = [a R b R,R' L a'] = [a R L',L b R]
                            commuteCase = simplify(
                                part1x + invert([arr[i + j]]))
                            commuteAdd1.append(commuteCase)
                            commuteCase = simplify([arr[i + j]] + part2x)
                            commuteAdd2.append(commuteCase)
                            # For a R2 b R' L2 a' R' L' b' L' = [a R2 b L R,R2' L a'] = [a R2 L',L b R L]
                            if len(arr) >= i + j + 2:
                                if isSameClass(arr[i + j], arr[i + j + 1]):
                                    commuteCase = simplify(
                                        part1x + invert(arr[i + j:i + j + 2])
                                    )
                                    commuteAdd1.append(commuteCase)
                                    commuteCase = simplify(
                                        arr[i + j:i + j + 2] + part2x
                                    )
                                    commuteAdd2.append(commuteCase)
                    for commuteAddKey in range(len(commuteAdd1)):
                        part1x = commuteAdd1[commuteAddKey]
                        part2x = commuteAdd2[commuteAddKey]
                        subArr = simplify(
                            part2x + part1x + invert(part2x) + invert(part1x) + arr)
                        subPart = ""
                        if depth > 1:
                            subPart = commutatorPre(
                                subArr, depth - 1, maxSubDepth)[0]
                        elif len(subArr) > 0:
                            continue
                        if subPart != "Not found.":
                            part1y = part1x
                            part2y = part2x
                            party = simplify(part2x + part1x)
                            if len(party) < max(len(part1x), len(part2x)):
                                if len(part1x) <= len(part2x):
                                    # For a b c d e b' a' c' e' d' = [a b c,d e b' a'] = [a b c,d e c]
                                    part1y = part1x
                                    part2y = party
                                else:
                                    # For a b c d e b' a' d' c' e' = [a b c,d e b' a'] = [a b c d,e b' a']
                                    part1y = invert(part2x)
                                    part2y = party
                            part0 = simplify(repeatEnd(arrBak[:d], dr))
                            part1 = part1y
                            part2 = part2y
                            if len(part0) and maxSubDepth == 1:
                                partz = simplify(part0 + part2y)
                                if len(partz) < len(part0) - 1:
                                    part0 = partz
                                    part1 = invert(part2y)
                                    part2 = part1y
                            part1Output = arrayToStr(part1)
                            part2Output = arrayToStr(part2)
                            part0Output = arrayToStr(part0)
                            if not len(part1Output) or not len(part2Output):
                                continue
                            commutatorStr = pairToStr(
                                part0Output, part1Output, part2Output, subPart)
                            if commutatorOutput == "":
                                commutatorOutput = commutatorStr
                            if score(commutatorStr) < score(commutatorOutput):
                                commutatorOutput = commutatorStr
                            if depth == maxSubDepth and commutatorStr not in result:
                                result.append(commutatorStr)
                            if fast:
                                return [commutatorOutput]
    if commutatorOutput == "":
        return ["Not found."]
    return [commutatorOutput]


def repeatEnd(array: List[Move], attempt: int) -> List[Move]:
    arr = array.copy()
    if len(arr) == 0:
        return []
    arrPop = arr.pop()
    if attempt == 0:
        return arr
    arr.append(Move(arrPop.base, attempt))
    return arr


def pairToStr(part0: str, part1: str, part2: str, subPart: str) -> str:
    if subPart == "":
        if not outerBracket:
            if part0 == "":
                return f"[{part1},{part2}]"
            return f"{part0}:[{part1},{part2}]"
        elif part0 == "":
            return f"[{part1},{part2}]"
        return f"[{part0}:[{part1},{part2}]]"
    if not outerBracket:
        if part0 == "":
            return f"[{part1},{part2}]+{subPart}"
        return f"{part0}:[[{part1},{part2}]+{subPart}]"
    elif part0 == "":
        return f"[{part1},{part2}]{subPart}"
    return f"[{part0}:[{part1},{part2}]{subPart}]"


def displace(array: List[Move], d: int, dr: int) -> List[Move]:
    arr = array.copy()
    arrEnd = repeatEnd(arr[:d], dr)
    return simplify(invert(arrEnd) + arr + arrEnd)


def invert(array: List[Move]) -> List[Move]:
    arr = []
    for i in range(len(array) - 1, -1, -1):
        arr.append(Move(array[i].base, normalize(-array[i].amount)))
    return arr


def algToArray(algorithm: str) -> List[Move]:
    global maxAlgAmount
    algTemp = algorithm
    for s in initialReplace:
        re_ = re.compile(s)
        algTemp = re.sub(re_, initialReplace[s], algTemp)
    algTemp = algTemp.replace(" ", "")
    algTemp = algTemp.replace("‘", "'")
    algTemp = algTemp.replace("’", "'")
    if algTemp == "":
        return []
    alg = ""
    for i in range(len(algTemp)):
        if (i < len(algTemp) - 1 and
            (algTemp[i + 1] < "0" or algTemp[i + 1] > "9") and
            algTemp[i + 1] != "'"
            ):
            alg += algTemp[i] + " "
        else:
            alg += algTemp[i]
    algSplit = alg.split(" ")
    arr = []
    for i in range(len(algSplit)):
        arr.append(Move(algSplit[i][0], 0))
        algNumber = re.sub(r"[^0-9]", "", algSplit[i])
        if algNumber == "":
            arr[i].amount = 1
        else:
            arr[i].amount = int(algNumber)
        if arr[i].amount > maxAlgAmount:
            maxAlgAmount = arr[i].amount
        if "'" in algSplit[i]:
            arr[i].amount = -arr[i].amount
    return arr


def arrayToStr(array: List[Move]) -> str:
    arr = array.copy()
    arr = simplify(arr)
    if len(arr) == 0:
        return ""
    isChanged = True
    while isChanged:
        isChanged = False
        for i in range(len(arr) - 1):
            if isSameClass(arr[i], arr[i + 1]) and commute[arr[i].base]["priority"] > commute[arr[i + 1].base]["priority"]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                isChanged = True
    arrTemp = []
    for i in range(len(arr)):
        if arr[i].amount < 0:
            if arr[i].amount == -1:
                arrTemp.append(f"{arr[i].base}'")
            else:
                arrTemp.append(f"{arr[i].base}{-arr[i].amount}'")
        elif arr[i].amount == 1:
            arrTemp.append(arr[i].base)
        else:
            arrTemp.append(f"{arr[i].base}{arr[i].amount}")
    arrOutput = f"{' '.join(arrTemp)} "
    for s in finalReplace:
        arrOutput = arrOutput.replace(f"{s} ", f"{finalReplace[s]} ")
    arrOutput = arrOutput[:-1]
    return arrOutput


def simplify(array: List[Move]) -> List[Move]:
    if len(array) == 0:
        return []
    arr: List[Move] = []
    max_priority = max(sum(1 for value in commute.values() if value['class'] == class_num) for class_num in set(
        value['class'] for value in commute.values())) if commute else 1
    for i in range(len(array)):
        arrayAdd = Move(array[i].base, normalize(array[i].amount))
        arrLen = len(arr)
        if normalize(arrayAdd.amount) == 0:
            continue
        isChange = False
        for j in range(1, max_priority + 1):
            if len(arr) >= j:
                if arr[arrLen - j].base == arrayAdd.base:
                    canCommute = True
                    if j >= 2:
                        for k in range(1, j + 1):
                            if arr[arrLen - k].base not in commute:
                                canCommute = False
                                break
                        for k in range(2, j + 1):
                            if not isSameClass(arr[arrLen - k], arr[arrLen - (k - 1)]):
                                canCommute = False
                                break
                    if canCommute:
                        moveAdd = Move(
                            arr[arrLen - j].base, normalize(arr[arrLen - j].amount + arrayAdd.amount))
                        if moveAdd.amount == 0:
                            arr.pop(-j)
                        else:
                            arr[-j] = moveAdd
                        isChange = True
                        break
        if not isChange:
            arr.append(arrayAdd)
    return arr


def isSameClass(move1: Move, move2: Move) -> bool:
    if (move1.base in commute) and (move2.base in commute):
        if commute[move1.base]["class"] == commute[move2.base]["class"]:
            return True
    return False


def normalize(amount: int) -> int:
    if isOrderZero:
        return amount
    return (((amount % order) + order - minAmount) % order) + minAmount
