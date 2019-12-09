import unittest

from intcode import runProgramIO


class Day5(unittest.TestCase):
    def setUp(self):
        with open('input5') as fh:
            self.program = [int(i) for i in fh.readline().split(',')]

    def testPart1(self):
        output = runProgramIO(self.program, [1])
        self.assertEqual(output[-1], 13547311)

    def testPart2(self):
        output = runProgramIO(self.program, [5])
        self.assertEqual(output[-1], 236453)

    def testComparePosition(self):
        # output 1 if input is equal to 8, 0 otherwise
        self.assertEqual(runProgramIO([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [5]), [0])
        self.assertEqual(runProgramIO([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8]), [1])
        self.assertEqual(runProgramIO([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [10]), [0])

        # output 1 if input is less than 8, 0 otherwise
        self.assertEqual(runProgramIO([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [5]), [1])
        self.assertEqual(runProgramIO([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8]), [0])
        self.assertEqual(runProgramIO([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [10]), [0])

    def testCompareImmediate(self):
        # output 1 if input is equal to 8, 0 otherwise
        self.assertEqual(runProgramIO([3, 3, 1108, -1, 8, 3, 4, 3, 99], [5]), [0])
        self.assertEqual(runProgramIO([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8]), [1])
        self.assertEqual(runProgramIO([3, 3, 1108, -1, 8, 3, 4, 3, 99], [10]), [0])

        # output 1 if input is less than 8, 0 otherwise
        self.assertEqual(runProgramIO([3, 3, 1107, -1, 8, 3, 4, 3, 99], [5]), [1])
        self.assertEqual(runProgramIO([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8]), [0])
        self.assertEqual(runProgramIO([3, 3, 1107, -1, 8, 3, 4, 3, 99], [10]), [0])

    def testJumpPosition(self):
        # output 0 if the input is 0, 1 otherwise
        self.assertEqual(runProgramIO([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [-5]), [1])
        self.assertEqual(runProgramIO([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0]), [0])
        self.assertEqual(runProgramIO([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [5]), [1])

    def testJumpImmediate(self):
        # output 0 if the input is 0, 1 otherwise
        self.assertEqual(runProgramIO([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [-5]), [1])
        self.assertEqual(runProgramIO([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]), [0])
        self.assertEqual(runProgramIO([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [5]), [1])

    def testLargerExample(self):
        # output 999 if the input is less than 8, 1000 if the input is equal to 8, 1001 otherwise
        program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
        self.assertEqual(runProgramIO([n for n in program], [5]), [999])
        self.assertEqual(runProgramIO([n for n in program], [8]), [1000])
        self.assertEqual(runProgramIO([n for n in program], [10]), [1001])


if __name__ == '__main__':
    unittest.main()
