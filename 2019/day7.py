from queue import Queue
from threading import Thread

import unittest


def evalProgram(program, read, write):
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
            program[arg1] = read()
            return pc + 2
        elif opcode == OUT:
            arg1 = argv(pc + 1, mode1)
            write(arg1)
            return pc + 2
        elif opcode == HALT:
            return -1

    pc = 0
    while 0 <= pc < len(program):
        pc = evalInstr(pc)


def thrusterSignal(program, phaseSettings):
    programs = [[n for n in program] for _ in phaseSettings]
    inputs = [Queue() for _ in phaseSettings]
    outputs = [[] for _ in phaseSettings]

    def runProgram(i):
        def read():
            return inputs[i].get()

        def write(n):
            outputs[i].append(n)
            inputs[(i + 1) % len(inputs)].put(n)

        evalProgram(programs[i], read, write)

    for i, p in enumerate(phaseSettings):
        inputs[i].put(p)
        if i == 0:
            inputs[0].put(0)  # first input

    threads = [Thread(target=runProgram, args=(i,)) for i in range(len(programs))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return outputs[-1][-1]  # last output


def maxSignal(program, phaseSettings):
    maxOutput, maxPhaseSetting = None, None

    for phaseSetting in perms(phaseSettings):
        output = thrusterSignal(program, phaseSetting)
        if maxOutput is None or output > maxOutput:
            maxOutput, maxPhaseSetting = output, phaseSetting

    return maxOutput, maxPhaseSetting


def perms(seq):
    if len(seq) == 0:
        return [[]]
    result = []
    first, rest = seq[0], seq[1:]
    for perm in perms(rest):
        for i in range(len(seq)):
            result.append(perm[:i] + [first] + perm[i:])
    return result


class Day7(unittest.TestCase):
    def setUp(self):
        with open('input7') as fh:
            self.program = [int(i) for i in fh.readline().split(',')]

    def testPart1(self):
        signal, _ = maxSignal(self.program, [0, 1, 2, 3, 4])
        self.assertEqual(signal, 338603)

    def testPart2(self):
        signal, _ = maxSignal(self.program, [5, 6, 7, 8, 9])
        self.assertEqual(signal, 63103596)

    def testSimple(self):
        program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
        signal, phaseSetting = maxSignal(program, [0, 1, 2, 3, 4])
        self.assertEqual(signal, 43210)
        self.assertEqual(phaseSetting, [4, 3, 2, 1, 0])

    def testLoop(self):
        program = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                   27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
        signal, phaseSetting = maxSignal(program, [5, 6, 7, 8, 9])
        self.assertEqual(signal, 139629729)
        self.assertEqual(phaseSetting, [9, 8, 7, 6, 5])


if __name__ == '__main__':
    unittest.main()
