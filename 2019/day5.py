import unittest


def evalProgram(program, inputValues):
    output = []

    ADD, MUL, IN, OUT, JNZ, JZ, LT, EQ, HALT = 1, 2, 3, 4, 5, 6, 7, 8, 99

    binop = {ADD: lambda a, b: a + b, MUL: lambda a, b: a * b,
             LT: lambda a, b: int(a < b), EQ: lambda a, b: int(a == b)}

    jop = {JNZ: lambda a: a != 0, JZ: lambda a: a == 0}

    def argv(i, mode):
        return program[program[i]] if mode == 0 else program[i]

    def evalInstr(pc):
        instr = str(program[pc]).zfill(5)
        opcode, mode1, mode2 = int(instr[3:]), int(instr[2]), int(instr[1])

        if opcode in binop:
            arg1 = argv(pc + 1, mode1)
            arg2 = argv(pc + 2, mode2)
            arg3 = program[pc + 3]
            program[arg3] = binop[opcode](arg1, arg2)
            return pc + 4
        elif opcode in jop:
            arg1 = argv(pc + 1, mode1)
            arg2 = argv(pc + 2, mode2)
            return arg2 if jop[opcode](arg1) else pc + 3
        elif opcode == IN:
            arg1 = program[pc + 1]
            program[arg1] = inputValues.pop()
            return pc + 2
        elif opcode == OUT:
            arg1 = program[pc + 1]
            output.append(program[arg1])
            return pc + 2
        elif opcode == HALT:
            return -1

    pc = 0
    while 0 <= pc < len(program):
        pc = evalInstr(pc)

    return output


class Day5(unittest.TestCase):
    def setUp(self):
        with open('input5') as fh:
            self.program = [int(i) for i in fh.readline().split(',')]

    def testPart1(self):
        output = evalProgram(self.program, [1])
        self.assertEqual(output[-1], 13547311)

    def testPart2(self):
        output = evalProgram(self.program, [5])
        self.assertEqual(output[-1], 236453)

    def testComparePosition(self):
        # output 1 if input is equal to 8, 0 otherwise
        self.assertEqual(evalProgram([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [5]), [0])
        self.assertEqual(evalProgram([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8]), [1])
        self.assertEqual(evalProgram([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [10]), [0])

        # output 1 if input is less than 8, 0 otherwise
        self.assertEqual(evalProgram([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [5]), [1])
        self.assertEqual(evalProgram([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8]), [0])
        self.assertEqual(evalProgram([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [10]), [0])

    def testCompareImmediate(self):
        # output 1 if input is equal to 8, 0 otherwise
        self.assertEqual(evalProgram([3, 3, 1108, -1, 8, 3, 4, 3, 99], [5]), [0])
        self.assertEqual(evalProgram([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8]), [1])
        self.assertEqual(evalProgram([3, 3, 1108, -1, 8, 3, 4, 3, 99], [10]), [0])

        # output 1 if input is less than 8, 0 otherwise
        self.assertEqual(evalProgram([3, 3, 1107, -1, 8, 3, 4, 3, 99], [5]), [1])
        self.assertEqual(evalProgram([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8]), [0])
        self.assertEqual(evalProgram([3, 3, 1107, -1, 8, 3, 4, 3, 99], [10]), [0])

    def testJumpPosition(self):
        # output 0 if the input is 0, 1 otherwise
        self.assertEqual(evalProgram([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [-5]), [1])
        self.assertEqual(evalProgram([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0]), [0])
        self.assertEqual(evalProgram([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [5]), [1])

    def testJumpImmediate(self):
        # output 0 if the input is 0, 1 otherwise
        self.assertEqual(evalProgram([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [-5]), [1])
        self.assertEqual(evalProgram([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]), [0])
        self.assertEqual(evalProgram([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [5]), [1])

    def skip_testLargerExample(self):  # TODO?
        # output 999 if the input is less than 8, 1000 if the input is equal to 8, 1001 otherwise
        program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
        self.assertEqual(evalProgram([n for n in program], [5]), [999])
        self.assertEqual(evalProgram([n for n in program], [8]), [1000])
        self.assertEqual(evalProgram([n for n in program], [10]), [1001])


if __name__ == '__main__':
    unittest.main()
