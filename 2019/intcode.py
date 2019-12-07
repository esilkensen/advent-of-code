def evalProgram(program, read=None, write=None):
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
