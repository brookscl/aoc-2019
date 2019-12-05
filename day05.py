def create_code_list(input):
    return [int(x) for x in input.split(",")]


def create_code_string(code_list):
    return ','.join(map(str, code_list))


OP_CODES = {
    99: 0,
    1: 4,
    2: 4,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 4,
    8: 4
}


def get_param(pos, mode, code_list):
    if mode == 0:  # position mode
        return code_list[code_list[pos]]
    else:          # immediate mode
        return code_list[pos]


def compute(code_list, input_entry=None):
    if isinstance(code_list, str):
        code_list = create_code_list(code_list)
    output = None
    pc = 0
    while True:
        op = code_list[pc]
        str_op = str(op).zfill(5)
        op = int(str_op[-2:])
        mode_1 = int(str_op[-3])
        mode_2 = int(str_op[-4])
        # mode_3 = int(str_op[-5])
        increment = OP_CODES[op]
        # Halt
        if op == 99:
            break
        # Addition
        if op == 1:
            a = get_param(pc + 1, mode_1, code_list)
            b = get_param(pc + 2, mode_2, code_list)
            code_list[code_list[pc + 3]] = a + b
            pc += increment
        # Multply
        if op == 2:
            a = get_param(pc + 1, mode_1, code_list)
            b = get_param(pc + 2, mode_2, code_list)
            code_list[code_list[pc + 3]] = a * b
            pc += increment
        # Input
        if op == 3:
            if input_entry is None:
                input_entry = int(input('Enter the integer input:'))
            code_list[code_list[pc + 1]] = input_entry
            pc += increment
        # Output
        if op == 4:
            output = code_list[code_list[pc + 1]]
            print(f"OUTPUT: {code_list[code_list[pc + 1]]}")
            pc += increment
        # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        if op == 5:
            if get_param(pc + 1, mode_1, code_list):
                pc = get_param(pc + 2, mode_2, code_list)
            else:
                pc += increment
        # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        if op == 6:
            if not get_param(pc + 1, mode_1, code_list):
                pc = get_param(pc + 2, mode_2, code_list)
            else:
                pc += increment
        # Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        if op == 7:
            if get_param(pc + 1, mode_1, code_list) < get_param(pc + 2, mode_2, code_list):
                code_list[code_list[pc + 3]] = 1
            else:
                code_list[code_list[pc + 3]] = 0
            pc += increment
        # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        if op == 8:
            if get_param(pc + 1, mode_1, code_list) == get_param(pc + 2, mode_2, code_list):
                code_list[code_list[pc + 3]] = 1
            else:
                code_list[code_list[pc + 3]] = 0
            pc += increment
    return output


assert compute("3,0,4,0,99", 1) == 1


input_str = """3,225,1,225,6,6,1100,1,238,225,104,0,1101,90,64,225,1101,15,56,225,1,
14,153,224,101,-147,224,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,2,162,
188,224,101,-2014,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1001,18,
81,224,1001,224,-137,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,16,
16,224,101,-256,224,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,101,48,
217,224,1001,224,-125,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,1002,
158,22,224,1001,224,-1540,224,4,224,1002,223,8,223,101,2,224,224,1,223,224,223,
1101,83,31,225,1101,56,70,225,1101,13,38,225,102,36,192,224,1001,224,-3312,224,4,
224,1002,223,8,223,1001,224,4,224,1,224,223,223,1102,75,53,225,1101,14,92,225,
1101,7,66,224,101,-73,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1101,
77,60,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,
1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,
99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,
225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,
314,0,0,106,0,0,1105,1,99999,7,226,677,224,1002,223,2,223,1005,224,329,1001,223,1,
223,1007,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,108,226,226,224,1002,
223,2,223,1006,224,359,101,1,223,223,7,226,226,224,102,2,223,223,1005,224,374,101,
1,223,223,8,677,677,224,1002,223,2,223,1005,224,389,1001,223,1,223,107,677,677,224,
102,2,223,223,1006,224,404,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,
419,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,434,1001,223,1,223,7,
677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,1107,226,226,224,1002,223,2,
223,1005,224,464,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,479,101,1,
223,223,1007,677,677,224,102,2,223,223,1006,224,494,1001,223,1,223,1107,226,677,224,
1002,223,2,223,1005,224,509,101,1,223,223,1007,226,226,224,1002,223,2,223,1006,224,
524,101,1,223,223,107,226,226,224,1002,223,2,223,1005,224,539,1001,223,1,223,1108,
677,677,224,1002,223,2,223,1005,224,554,101,1,223,223,1008,677,226,224,102,2,223,
223,1006,224,569,1001,223,1,223,8,226,677,224,102,2,223,223,1005,224,584,1001,223,
1,223,1008,677,677,224,1002,223,2,223,1006,224,599,1001,223,1,223,108,677,677,224,
102,2,223,223,1006,224,614,1001,223,1,223,108,226,677,224,102,2,223,223,1005,224,
629,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,107,677,
226,224,1002,223,2,223,1005,224,659,101,1,223,223,1108,677,226,224,102,2,223,223,
1005,224,674,1001,223,1,223,4,223,99,226"""


# Part 1
assert compute(input_str, 1) == 7988899


# Part 2
assert compute("3,9,8,9,10,9,4,9,99,-1,8", 1) == 0
assert compute("3,9,8,9,10,9,4,9,99,-1,8", 8) == 1

compute(input_str, 5)
