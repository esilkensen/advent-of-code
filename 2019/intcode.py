from collections import defaultdict


ADD, MUL, IN, OUT, JNZ, JZ, LT, EQ, RB, HALT = 1, 2, 3, 4, 5, 6, 7, 8, 9, 99
POS, IMM, OFF = 0, 1, 2

BINOP = {ADD: lambda a, b: a + b, MUL: lambda a, b: a * b,
         LT: lambda a, b: int(a < b), EQ: lambda a, b: int(a == b)}

JOP = {JNZ: lambda a: a != 0, JZ: lambda a: a == 0}


class Intcode:
    def __init__(self, program, read=None, write=None):
        self._program = [n for n in program]
        self._read = read
        self._write = write

    def run(self):
        self.mem = defaultdict(int)
        for i, n in enumerate(self._program):
            self.mem[i] = n

        self.pc, self.rb = 0, 0
        while self.pc != -1:
            self.step()

        return self.mem

    def step(self):
        instr = str(self.mem[self.pc]).zfill(5)
        opcode, modes = int(instr[3:]), [int(d) for d in instr[2::-1]]

        if opcode in BINOP:
            self.binop(opcode, modes)
        elif opcode in JOP:
            self.jop(opcode, modes)
        elif opcode == IN:
            self.read(modes)
        elif opcode == OUT:
            self.write(modes)
        elif opcode == RB:
            self.offset(modes)
        elif opcode == HALT:
            self.halt()

    def binop(self, opcode, modes):
        arg1 = self.argv(1, modes[0])
        arg2 = self.argv(2, modes[1])
        arg3 = self.argv(3, modes[2], deref=False)
        self.mem[arg3] = BINOP[opcode](arg1, arg2)
        self.pc += 4

    def jop(self, opcode, modes):
        arg1 = self.argv(1, modes[0])
        arg2 = self.argv(2, modes[1])
        self.pc = arg2 if JOP[opcode](arg1) else self.pc + 3

    def read(self, modes):
        arg1 = self.argv(1, modes[0], deref=False)
        self.mem[arg1] = self._read()
        self.pc += 2

    def write(self, modes):
        arg1 = self.argv(1, modes[0])
        self._write(arg1)
        self.pc += 2

    def offset(self, modes):
        arg1 = self.argv(1, modes[0])
        self.rb += arg1
        self.pc += 2

    def halt(self):
        self.pc = -1

    def argv(self, i, mode, deref=True):
        base = self.pc + i
        offset = self.rb if mode == OFF else 0
        addr = base if mode == IMM else self.mem[base] + offset
        return self.mem[addr] if deref else addr


def runProgram(program, read=None, write=None):
    return Intcode(program, read, write).run()


def runProgramIO(program, inputValues):
    outputValues = []
    runProgram(program, inputValues.pop, outputValues.append)
    return outputValues
