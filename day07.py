import itertools


def create_code_list(input):
    return [int(x) for x in input.split(",")]


def create_code_string(code_list):
    return ",".join(map(str, code_list))


OP_CODES = {99: 0, 1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}


class ComputerState:
    def __init__(self, modes, pc, code_list):
        self.modes = modes
        self.pc = pc
        self.code_list = code_list

    def get_param(self, param):
        if self.modes[param - 1] == 0:  # position mode
            return self.code_list[self.code_list[self.pc + param]]
        else:  # immediate mode
            return self.code_list[self.pc + param]

    halted = False


def compute(code_list, input_entry=None, amp=None, state=None):
    if isinstance(code_list, str):
        code_list = create_code_list(code_list)
    output = None
    if state:
        pc = state.pc
        # pc = 0
        code_list = state.code_list
    else:
        pc = 0

    while True:
        op = code_list[pc]
        str_op = str(op).zfill(5)
        op = int(str_op[-2:])
        modes = [int(str_op[-3]), int(str_op[-4])]
        c = ComputerState(modes, pc, code_list)
        increment = OP_CODES[op]
        # Halt
        if op == 99:
            output = input_entry[0]
            c.halted = True
            break
        # Addition
        if op == 1:
            a = c.get_param(1)
            b = c.get_param(2)
            code_list[code_list[pc + 3]] = a + b
            pc += increment
        # Multply
        if op == 2:
            a = c.get_param(1)
            b = c.get_param(2)
            code_list[code_list[pc + 3]] = a * b
            pc += increment
        # Input
        if op == 3:
            if input_entry is None:
                input_entry = [int(input("Enter the integer input:"))]
            code_list[code_list[pc + 1]] = input_entry[0]
            input_entry.pop(0)
            pc += increment
        # Output
        if op == 4:
            output = c.get_param(1)
            # print(f"OUTPUT: {output} for amp {amp}")
            # Save state
            c.halted = False
            pc += increment
            c.pc = pc
            c.code_list = code_list
            break
        # Opcode 5 is jump-if-true
        if op == 5:
            if c.get_param(1):
                pc = c.get_param(2)
            else:
                pc += increment
        # Opcode 6 is jump-if-false
        if op == 6:
            if not c.get_param(1):
                pc = c.get_param(2)
            else:
                pc += increment
        # Opcode 7 is less than
        if op == 7:
            if c.get_param(1) < c.get_param(2):
                code_list[code_list[pc + 3]] = 1
            else:
                code_list[code_list[pc + 3]] = 0
            pc += increment
        # Opcode 8 is equals
        if op == 8:
            if c.get_param(1) == c.get_param(2):
                code_list[code_list[pc + 3]] = 1
            else:
                code_list[code_list[pc + 3]] = 0
            pc += increment
    return (output, c)


# assert compute("3,0,4,0,99", [1]) == 1


def multiphase(program, phases):
    if isinstance(phases, str):
        phases = list(map(int, phases.split(',')))
    staged_input = 0
    amp = 0
    states = {}
    while True:
        state = None
        if amp in states:
            state = states[amp]
            feed_input = [staged_input]
        else:
            feed_input = [phases[amp], staged_input]
        (staged_input, state) = compute(program, feed_input, amp, state)
        if state.halted:
            break
        states[amp] = state
        amp = (amp + 1) % len(phases)


    return staged_input


# program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

# assert multiphase(program, "4,3,2,1,0") == 43210

# program = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"

# assert multiphase(program, "1,0,4,3,2") == 65210

# # Part 1

# with open("day07_program.txt") as f:
#     content = f.readlines()

# program = content[0].strip()

# phase_options = list(itertools.permutations([0, 1, 2, 3,4]))

# max_output = -1

# for phase_check in phase_options:
#     output = multiphase(program, phase_check)
#     if output > max_output:
#         max_output = output

# print(max_output)

# Part 2

# program = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

# print(multiphase(program, "9,8,7,6,5"))

# program = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"

# print(multiphase(program, "9,7,8,5,6"))


with open("day07_program.txt") as f:
    content = f.readlines()

program = content[0].strip()

phase_options = list(itertools.permutations([5, 6, 7, 8, 9]))

max_output = -1

for phase_check in phase_options:
    output = multiphase(program, phase_check)
    if output > max_output:
        print(f"Found new max: {output}")
        max_output = output
