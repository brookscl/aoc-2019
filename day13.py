import itertools
import numpy


def create_code_list(input):
    code_list_array = [int(x) for x in input.split(",")]
    return numpy.pad(code_list_array, (0, 100 * len(code_list_array)), "constant")


def create_code_string(code_list):
    return ",".join(map(str, code_list))


def get_input():
    if ball_x > paddle_x:
        return [1]
    elif ball_x < paddle_x:
        return [-1]
    else:
        return [0]


waiting_for_x = True
waiting_for_y = False
waiting_for_tile = False
block_tile_count = 0
current_x = 0
current_y = 0
ball_x = 0
ball_y = 0
paddle_x = 0
paddle_y = 0


def put_output(output):
    global waiting_for_x, waiting_for_y, waiting_for_tile
    global block_tile_count, current_x, current_y, ball_x, ball_y
    global paddle_x, paddle_y
    if waiting_for_x:
        current_x = output
        waiting_for_y = True
        waiting_for_x = False
    elif waiting_for_y:
        current_y = output
        waiting_for_tile = True
        waiting_for_y = False
    else:
        if current_x == -1 and current_y == 0:
            print(f"Score: {output}")
        elif output == 2:  # Block
            block_tile_count += 1
        elif output == 3:  # Paddle
            paddle_x = current_x
            paddle_y = current_y
        elif output == 4:  # Ball
            ball_x = current_x
            ball_y = current_y
        waiting_for_tile = False
        waiting_for_x = True


class ComputerState:
    def __init__(self, pc, code_list):
        self.halted = False
        self.pc = pc
        self.code_list = code_list
        self.relative_base = 0

    def get_param(self, param):
        if self.modes[param - 1] == 0:  # position mode
            return self.code_list[self.code_list[self.pc + param]]
        elif self.modes[param - 1] == 1:  # immediate mode
            return self.code_list[self.pc + param]
        elif self.modes[param - 1] == 2:  # relative mode
            return self.code_list[self.code_list[self.pc + param] + self.relative_base]
        else:
            assert False, "Illegal parameter mode"

    def set_param(self, param, val):
        if self.modes[param - 1] == 0:  # position mode
            self.code_list[self.code_list[self.pc + param]] = val
        elif self.modes[param - 1] == 1:  # immediate mode
            self.code_list[self.pc + param] = val
        elif self.modes[param - 1] == 2:  # relative mode
            self.code_list[self.code_list[self.pc + param] + self.relative_base] = val
        else:
            assert False, "Illegal parameter mode"

    def fetch_op(self):
        op = self.code_list[self.pc]
        str_op = str(op).zfill(6)
        self.op = int(str_op[-2:])
        self.modes = [int(str_op[-3]), int(str_op[-4]), int(str_op[-5])]

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
        if input_entry:
            return input_entry[0]
        else:
            return None

    def add(self, _):
        a = self.get_param(1)
        b = self.get_param(2)
        self.set_param(3, a + b)
        self.increment_pc()
        return None

    def multiply(self, _):
        a = self.get_param(1)
        b = self.get_param(2)
        self.set_param(3, a * b)
        self.increment_pc()
        return None

    def input_op(self, input_entry):
        if input_entry is None:
            input_entry = get_input()

        self.set_param(1, input_entry[0])
        input_entry.pop(0)
        self.increment_pc()
        return None

    def output_op(self, _):
        output = self.get_param(1)
        self.halted = False
        self.increment_pc()
        put_output(output)
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
            self.set_param(3, 1)
        else:
            self.set_param(3, 0)
        self.increment_pc()
        return None

    # Op 8
    def equals(self, _):
        if self.get_param(1) == self.get_param(2):
            self.set_param(3, 1)
        else:
            self.set_param(3, 0)
        self.increment_pc()
        return None

    def adjust_relative_base(self, _):
        self.relative_base += self.get_param(1)
        self.increment_pc()
        return None

    OP_CODES = {
        1: {"jump": 4, "op": add},
        2: {"jump": 4, "op": multiply},
        3: {"jump": 2, "op": input_op},
        4: {"jump": 2, "op": output_op},
        5: {"jump": 3, "op": jump_if_true},
        6: {"jump": 3, "op": jump_if_false},
        7: {"jump": 4, "op": less_than},
        8: {"jump": 4, "op": equals},
        9: {"jump": 2, "op": adjust_relative_base},
        99: {"jump": 0, "op": halt},
    }


def compute(code_list, input_entry=None, amp=None, state=None):
    if isinstance(code_list, str):
        code_list = create_code_list(code_list)
    output = None
    if not state:
        state = ComputerState(0, code_list)

    while True:
        state.fetch_op()

        output = state.run_op(input_entry)
        if state.break_out:
            break

    return (output, state)


# Part 1

with open("day13_program.txt") as f:
    content = f.readlines()

program = content[0].strip()

(output, state) = compute(program)

print(f"Number of blocks: {block_tile_count}")


# Part 2

# Memory address 0 represents the number of quarters
# that have been inserted; set it to 2 to play for free

code_list = create_code_list(program)
code_list[0] = 2
(output, state) = compute(code_list)
