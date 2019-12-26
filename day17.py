from collections import namedtuple
from queue import Queue
import itertools
import numpy

Point = namedtuple("Point", "x y")

scaffold_set = set()
x = 0
y = 0


def get_input():
    assert False, "Shouldn't need input"


def put_output(output):
    global x, y

    if output == 35:
        scaffold_set.add(Point(x, y))
    if output == 10:
        x = 0
        y += 1
    else:
        x += 1
    print(chr(output), end="")


def create_code_list(input):
    code_list_array = [int(x) for x in input.split(",")]
    return numpy.pad(code_list_array, (0, 100 * len(code_list_array)), "constant")


def create_code_string(code_list):
    return ",".join(map(str, code_list))


class ComputerState:
    def __init__(
        self, pc, code_list, halt_on_output=False, input_func=None, output_func=None
    ):
        self.halted = False
        self.halt_on_output = halt_on_output
        self.pc = pc
        if isinstance(code_list, str):
            code_list = create_code_list(code_list)
        self.code_list = code_list
        self.relative_base = 0
        self.input_func = input_func
        self.output_func = output_func

    def clone(self):
        copy = ComputerState(
            self.pc,
            self.code_list.copy(),
            self.halt_on_output,
            self.input_func,
            self.output_func,
        )
        return copy

    def run(self, input_entry=None):

        output = None

        while True:
            self.fetch_op()

            output = self.run_op(input_entry)
            if self.break_out:
                break

        return output

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
            input_entry = self.input_func()

        self.set_param(1, input_entry[0])
        input_entry.pop(0)
        self.increment_pc()
        return None

    def output_op(self, _):
        output = self.get_param(1)
        self.halted = self.halt_on_output
        self.break_out = self.halt_on_output
        self.increment_pc()
        if self.output_func:
            self.output_func(output)
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


ALLOWED_MOVES = {
    1: Point(0, 1),
    2: Point(0, -1),
    3: Point(1, 0),
    4: Point(-1, 0),
}


def move(start, direction):
    x = start.x + ALLOWED_MOVES[direction].x
    y = start.y + ALLOWED_MOVES[direction].y
    return Point(x, y)


# Part 1


def find_intersections(scaffolding):
    intersections = []
    for scaffold in scaffolding:
        intersection = True
        for adjacent in range(1, 5):
            if move(scaffold, adjacent) not in scaffolding:
                intersection = False
                break
        if intersection:
            intersections.append(scaffold)
    return intersections


with open("day17_program.txt") as f:
    content = f.readlines()

program = content[0].strip()
code_list = create_code_list(program)

start_state = ComputerState(0, code_list, output_func=put_output)
start_state.run()

intersections = find_intersections(scaffold_set)
print(f"Found {len(intersections)} intersections")
print(f"List: {intersections}")
alignment_sum = sum(p.x * p.y for p in intersections)
print(f"Sum of alignment params: {alignment_sum}")
