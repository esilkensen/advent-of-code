from collections import defaultdict
import unittest

from intcode import evalProgram


def run(program, inputValues):
    outputValues = []

    def read():
        return inputValues.pop()

    def write(n):
        outputValues.append(n)

    evalProgram(boostMemory(program), read, write)
    return outputValues


def boostMemory(program):
    boosted = defaultdict(int)
    for i, n in enumerate(program):
        boosted[i] = n
    return boosted


class Day9(unittest.TestCase):
    def setUp(self):
        with open('input9') as fh:
            self.program = [int(i) for i in fh.readline().split(',')]

    def testPart1(self):
        self.assertEqual(run(self.program, [1]), [2316632620])

    def testPart2(self):
        self.assertEqual(run(self.program, [2]), [78869])

    def testQuine(self):
        program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        self.assertEqual(run(program, []), program)

    def testBigNumber(self):
        program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        self.assertEqual(run(program, []), [1219070632396864])

    def testMiddleNumber(self):
        program = [104, 1125899906842624, 99]
        self.assertEqual(run(program, []), [1125899906842624])


if __name__ == '__main__':
    unittest.main()
