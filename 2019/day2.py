import unittest

from intcode import runProgram


def run(program, noun, verb):
    program[1] = noun
    program[2] = verb
    return runProgram(program)[0]


def search(program, target):
    for noun in range(100):
        for verb in range(100):
            if run(program, noun, verb) == target:
                return 100 * noun + verb


class Day2(unittest.TestCase):
    def setUp(self):
        with open('input2') as fh:
            self.program = [int(i) for i in fh.readline().split(',')]

    def testPart1(self):
        self.assertEqual(run(self.program, 12, 2), 3516593)

    def testPart2(self):
        self.assertEqual(search(self.program, 19690720), 7749)


if __name__ == '__main__':
    unittest.main()
