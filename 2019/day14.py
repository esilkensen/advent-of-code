from collections import Counter, deque
import math
import unittest


def canProduceGiven(target, n, source, reactions):
    """
    How much of a target chemical can be produced given an amount (n) of a source chemical.
    """
    start = requiredToProduce(source, 1, target, reactions)
    end, m = start, 1
    while end < n:
        start, m = m, m * 2
        end = requiredToProduce(source, m, target, reactions)

    while start <= end:
        mid = (start + end) // 2
        m = requiredToProduce(source, mid, target, reactions)
        if m < n:
            start = mid + 1
        elif m > n:
            end = mid - 1
        else:
            return m

    return end


def requiredToProduce(source, n, target, reactions):
    """
    How much of a source chemical is required to produce an amount (n) of a target chemical.
    """
    required = Counter()
    balance = Counter()

    Q = deque(needed(n, target, balance, reactions))

    while len(Q) > 0:
        n, c = Q.popleft()
        if n <= balance[c]:
            balance[c] -= n
        elif c in reactions:
            lhs = needed(n, c, balance, reactions)
            for r, d in lhs:
                # TODO: clean this up
                combined = False
                for i, (r2, d2) in enumerate(Q):
                    if d == d2:
                        Q[i] = (r + r2, d)
                        combined = True
                        break
                if not combined:
                    Q.append((r, d))
        else:
            required[c] += n

    return required[source]


def needed(n, target, balance, reactions):
    p, lhs = reactions[target]
    factor = 1 if p >= n + balance[target] else int(math.ceil(n / (p - balance[target])))
    balance[target] += (p * factor) - n

    result = []

    for r, d in lhs:
        r *= factor
        if balance[d] > 0:
            balance[d], r = max(0, balance[d] - r), max(0, r - balance[d])
        result.append((r, d))

    return result


def parseReactions(path='input14'):
    outputs = {}
    reactions = parseInput(path)
    for lhs, [n, c] in reactions:
        assert(c not in outputs)
        outputs[c] = (n, lhs)
    return outputs


def parseInput(path='input14'):
    with open(path) as fh:
        reactions = []
        for line in fh:
            lhs, rhs = [[(int(n), c) for [n, c] in
                        [p.strip().split(' ') for p in side.split(',')]]
                        for side in line.strip().split('=>')]
            reactions.append((lhs, rhs[0]))
        return reactions


class Day14(unittest.TestCase):
    def testPart1(self):
        reactions = parseReactions('input14')
        required = requiredToProduce('ORE', 1, 'FUEL', reactions)
        self.assertEqual(required, 97422)

    def testPart2(self):
        reactions = parseReactions('input14')
        possible = canProduceGiven('FUEL', 1000000000000, 'ORE', reactions)
        self.assertEqual(possible, 13108426)

    def testRequired1(self):
        reactions = parseReactions('input14-1')
        required = requiredToProduce('ORE', 1, 'FUEL', reactions)
        self.assertEqual(required, 31)

    def testRequired2(self):
        reactions = parseReactions('input14-2')
        required = requiredToProduce('ORE', 1, 'FUEL', reactions)
        self.assertEqual(required, 165)

    def testRequired3(self):
        reactions = parseReactions('input14-3')
        required = requiredToProduce('ORE', 1, 'FUEL', reactions)
        self.assertEqual(required, 13312)

    def testRequired4(self):
        reactions = parseReactions('input14-4')
        required = requiredToProduce('ORE', 1, 'FUEL', reactions)
        self.assertEqual(required, 180697)

    def testRequired5(self):
        reactions = parseReactions('input14-5')
        required = requiredToProduce('ORE', 1, 'FUEL', reactions)
        self.assertEqual(required, 2210736)

    def testGiven3(self):
        reactions = parseReactions('input14-3')
        possible = canProduceGiven('FUEL', 1000000000000, 'ORE', reactions)
        self.assertEqual(possible, 82892753)

    def testGiven4(self):
        reactions = parseReactions('input14-4')
        possible = canProduceGiven('FUEL', 1000000000000, 'ORE', reactions)
        self.assertEqual(possible, 5586022)

    def testGiven5(self):
        reactions = parseReactions('input14-5')
        possible = canProduceGiven('FUEL', 1000000000000, 'ORE', reactions)
        self.assertEqual(possible, 460664)


if __name__ == '__main__':
    unittest.main()
