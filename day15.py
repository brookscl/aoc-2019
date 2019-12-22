from collections import namedtuple
from queue import Queue
import itertools
import numpy

Point = namedtuple("Point", "x y")

ALLOWED_MOVES = {
    "1": Point(0, 1),
    "2": Point(0, -1),
    "3": Point(1, 0),
    "4": Point(-1, 0),
}
travel_path = []
discovered = set()
to_explore = Queue()
current_position = Point(0, 0)
pending_move = None
discovered.add(current_position)


def move(start, direction):
    x = start.x + ALLOWED_MOVES[str(direction)].x
    y = start.y + ALLOWED_MOVES[str(direction)].y
    return Point(x, y)


def create_code_list(input):
    code_list_array = [int(x) for x in input.split(",")]
    return numpy.pad(code_list_array, (0, 100 * len(code_list_array)), "constant")


def create_code_string(code_list):
    return ",".join(map(str, code_list))


def should_explore(point):
    return point not in discovered


def opposite_direction(direction):
    oppo = {1: 2, 2: 1, 3: 4, 4: 3}
    return oppo[direction]


# north (1), south (2), west (3), and east (4).
def get_input():
    global pending_move
    for i in range(1, 5):
        pending_move = move(current_position, i)
        if should_explore(pending_move):
            travel_path.append(i)
            return [i]
    # Must backtrack
    last_move = travel_path.pop()
    print(f"Backtracking from: {current_position}")
    return [opposite_direction(last_move)]


# 0: The repair droid hit a wall. Its position has not changed.
# 1: The repair droid has moved one step in the requested direction.
# 2: The repair droid has moved one step in the requested direction;
#    its new position is the location of the oxygen system.
def put_output(output):
    global current_position

    if output == 0:  # Wall
        # walls.add(pending_move)
        pass
    elif output == 1:  # Moved but not Oxygen
        current_position = pending_move
        discovered.add(current_position)
    elif output == 2:  # Found the Oxygen
        current_position = pending_move
        print(f"Found oxygen at {current_position}")
    else:
        print(f"Unknown output: {output}")
        assert False


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


with open("day15_program.txt") as f:
    content = f.readlines()

program = content[0].strip()

(output, state) = compute(program)

