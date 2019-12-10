import itertools


def create_code_list(input):
    return [int(x) for x in input.split(",")]


def create_code_string(code_list):
    return ",".join(map(str, code_list))


class ComputerState:
    def __init__(self, pc, code_list):
        self.halted = False
        self.pc = pc
        self.code_list = code_list

    def get_param(self, param):
        if self.modes[param - 1] == 0:  # position mode
            return self.code_list[self.code_list[self.pc + param]]
        else:  # immediate mode
            return self.code_list[self.pc + param]

    def fetch_op(self):
        op = self.code_list[self.pc]
        str_op = str(op).zfill(5)
        self.op = int(str_op[-2:])
        self.modes = [int(str_op[-3]), int(str_op[-4])]

    def jump(self):
        return self.OP_CODES[self.op]["jump"]

    def op_func(self, input_entry):
        return self.OP_CODES[self.op]["op"](self, input_entry)

    def increment_pc(self):
        self.pc += self.jump()

    def run_op(self, input_entry):
        self.break_out = False

        return self.op_func(input_entry)

    def halt(self, input_entry):
        self.halted = True
        self.break_out = True
        return input_entry[0]

    def add(self, _):
        a = self.get_param(1)
        b = self.get_param(2)
        self.code_list[self.code_list[self.pc + 3]] = a + b
        self.increment_pc()
        return None

    def multiply(self, _):
        a = self.get_param(1)
        b = self.get_param(2)
        self.code_list[self.code_list[self.pc + 3]] = a * b
        self.increment_pc()
        return None

    def input(self, input_entry):
        if input_entry is None:
            input_entry = [int(input("Enter the integer input:"))]
        self.code_list[self.code_list[self.pc + 1]] = input_entry[0]
        input_entry.pop(0)
        self.increment_pc()
        return None

    def output(self, _):
        output = self.get_param(1)
        self.halted = False
        self.break_out = True
        self.increment_pc()
        return output

    def jump_if_true(self, _):
        if self.get_param(1):
            self.pc = self.get_param(2)
        else:
            self.increment_pc()
        return None

    def jump_if_false(self, _):
        if not self.get_param(1):
            self.pc = self.get_param(2)
        else:
            self.increment_pc()
        return None

    def less_than(self, _):
        if self.get_param(1) < self.get_param(2):
            self.code_list[self.code_list[self.pc + 3]] = 1
        else:
            self.code_list[self.code_list[self.pc + 3]] = 0
        self.increment_pc()
        return None

    def equals(self, _):
        if self.get_param(1) == self.get_param(2):
            self.code_list[self.code_list[self.pc + 3]] = 1
        else:
            self.code_list[self.code_list[self.pc + 3]] = 0
        self.increment_pc()
        return None

    OP_CODES = {
        99: {"jump": 0, "op": halt},
        1: {"jump": 4, "op": add},
        2: {"jump": 4, "op": multiply},
        3: {"jump": 2, "op": input},
        4: {"jump": 2, "op": output},
        5: {"jump": 3, "op": jump_if_true},
        6: {"jump": 3, "op": jump_if_false},
        7: {"jump": 4, "op": less_than},
        8: {"jump": 4, "op": equals},
    }


def compute(code_list, input_entry=None, amp=None, state=None):
    output = None
    if not state:
        state = ComputerState(0, code_list)

    while True:
        state.fetch_op()

        output = state.run_op(input_entry)
        if state.break_out:
            break

    return (output, state)


def multiphase(program_string, phases):
    if isinstance(phases, str):
        phases = list(map(int, phases.split(",")))
    staged_input = 0
    amp = 0
    states = {}
    while True:
        program = create_code_list(program_string)

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


program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

assert multiphase(program, "4,3,2,1,0") == 43210

program = """3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,
33,31,31,1,32,31,31,4,31,99,0,0,0"""

assert multiphase(program, "1,0,4,3,2") == 65210

# Part 1

with open("day07_program.txt") as f:
    content = f.readlines()

program = content[0].strip()

phase_options = list(itertools.permutations([0, 1, 2, 3, 4]))

max_output = -1

for phase_check in phase_options:
    output = multiphase(program, phase_check)
    if output > max_output:
        max_output = output

print(f"Max output is: {max_output}")

# Part 2

program = """3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,
28,6,99,0,0,5"""

assert multiphase(program, "9,8,7,6,5") == 139629729

program = """3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,
54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,
1005,56,6,99,0,0,0,0,10"""

assert multiphase(program, "9,7,8,5,6") == 18216


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
