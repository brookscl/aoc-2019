import itertools
import numpy
from collections import namedtuple


Point = namedtuple("Point", "x y")

facings = [
    Point(0, 1),  # Up
    Point(1, 0),  # Right
    Point(0, -1),  # Down
    Point(-1, 0),  # Left
]


painted_once = set()
paint_grid = set()
robot_x = 0
robot_y = 0
robot_facing = 0
waiting_for_color = True


def create_code_list(input):
    code_list_array = [int(x) for x in input.split(",")]
    return numpy.pad(code_list_array, (0, 100 * len(code_list_array)), "constant")


def create_code_string(code_list):
    return ",".join(map(str, code_list))


def get_input():
    if Point(robot_x, robot_y) in paint_grid:
        return [1]
    else:
        return [0]


def put_output(output):
    global waiting_for_color, robot_facing, robot_x, robot_y

    if waiting_for_color:
        robot_location = Point(robot_x, robot_y)
        # print(f"Paint point {robot_location} color {output}")
        if output == 0:
            if robot_location in paint_grid:
                painted_once.add(robot_location)
                paint_grid.remove(robot_location)
        else:
            painted_once.add(robot_location)
            paint_grid.add(robot_location)
        waiting_for_color = False
    else:  # Changing direction
        if output == 0:
            dir_change = -1
            # print("Turning left, new position:")
        else:
            dir_change = 1
            # print("Turning right, new position:")
        robot_facing = (robot_facing + dir_change) % 4
        robot_x += facings[robot_facing].x
        robot_y += facings[robot_facing].y
        # print(f"    {Point(robot_x, robot_y)}")
        waiting_for_color = True


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
            # input_entry = [int(input("Enter the integer input:"))]

        self.set_param(1, input_entry[0])
        input_entry.pop(0)
        self.increment_pc()
        return None

    def output_op(self, _):
        output = self.get_param(1)
        self.halted = False
        # self.break_out = True
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

with open("day11_program.txt") as f:
    content = f.readlines()

program = content[0].strip()

(output, state) = compute(program)
print(
    f"Final grid: {len(paint_grid)} white, painted at least once: {len(painted_once)}"
)

# Part 2
painted_once = set()
paint_grid = set()
robot_x = 0
robot_y = 0
robot_facing = 0
waiting_for_color = True
paint_grid.add(Point(0, 0))
(output, state) = compute(program)

x_max = max(paint_grid, key=lambda item: item.x).x
x_min = min(paint_grid, key=lambda item: item.x).x
y_max = max(paint_grid, key=lambda item: item.y).y
y_min = min(paint_grid, key=lambda item: item.y).y
print(x_max)
print(x_min)
print(y_max)
print(y_min)

for y in range(y_max, y_min - 1, -1):
    for x in range(x_min, x_max + 1):
        if Point(x, y) in paint_grid:
            print("-*-", end="")
        else:
            print("   ", end="")
    print("")
