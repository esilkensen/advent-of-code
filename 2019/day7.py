from queue import Queue
from threading import Thread
import unittest

from intcode import runProgram


def thrusterSignal(program, phaseSettings):
    programs = [[n for n in program] for _ in phaseSettings]
    inputs = [Queue() for _ in phaseSettings]
    outputs = [[] for _ in phaseSettings]

    def run(i):
        def read():
            return inputs[i].get()

        def write(n):
            outputs[i].append(n)
            inputs[(i + 1) % len(inputs)].put(n)

        runProgram(programs[i], read, write)

    for i, p in enumerate(phaseSettings):
        inputs[i].put(p)
        if i == 0:
            inputs[0].put(0)  # first input

    threads = [Thread(target=run, args=(i,)) for i in range(len(programs))]
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
