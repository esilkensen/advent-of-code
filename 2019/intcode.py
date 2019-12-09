def evalProgram(program, read=None, write=None):
    ADD, MUL, IN, OUT, JNZ, JZ, LT, EQ, RB, HALT = 1, 2, 3, 4, 5, 6, 7, 8, 9, 99

    binop = {ADD: lambda a, b: a + b, MUL: lambda a, b: a * b,
             LT: lambda a, b: int(a < b), EQ: lambda a, b: int(a == b)}

    jop = {JNZ: lambda a: a != 0, JZ: lambda a: a == 0}

    rb = 0

    def argv(i, mode, deref=True):
        addr = program[i] if mode == 0 else i if mode == 1 else program[i] + rb
        return program[addr] if deref else addr

    def evalInstr(pc):
        nonlocal rb
        instr = str(program[pc]).zfill(5)
        opcode, mode1, mode2, mode3 = int(instr[3:]), int(instr[2]), int(instr[1]), int(instr[0])

        if opcode in binop:
            arg1 = argv(pc + 1, mode1)
            arg2 = argv(pc + 2, mode2)
            arg3 = argv(pc + 3, mode3, False)
            program[arg3] = binop[opcode](arg1, arg2)
            return pc + 4
        elif opcode in jop:
            arg1 = argv(pc + 1, mode1)
            arg2 = argv(pc + 2, mode2)
            return arg2 if jop[opcode](arg1) else pc + 3
        elif opcode == IN:
            arg1 = argv(pc + 1, mode1, False)
            program[arg1] = read()
            return pc + 2
        elif opcode == OUT:
            arg1 = argv(pc + 1, mode1)
            write(arg1)
            return pc + 2
        elif opcode == RB:
            arg1 = argv(pc + 1, mode1)
            rb += arg1
            return pc + 2
        elif opcode == HALT:
            return -1

    pc = 0
    while pc != -1:
        pc = evalInstr(pc)
