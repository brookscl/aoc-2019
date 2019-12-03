def create_code_list(input):
    return [int(x) for x in input.split(",")]


def create_code_string(code_list):
    return ','.join(map(str, code_list))


def compute(code_list, noun=None, verb=None):
    if isinstance(code_list, str):
        code_list = create_code_list(code_list)
    if noun:
        code_list[1] = noun
    if verb:
        code_list[2] = verb
    i = 0
    while True:
        base = 4 * i
        op = code_list[base]
        # Halt
        if op == 99:
            break
        # Addition
        if op == 1:
            a = code_list[code_list[base + 1]]
            b = code_list[code_list[base + 2]]
            code_list[code_list[base + 3]] = a + b
        # Multply
        if op == 2:
            a = code_list[code_list[base + 1]]
            b = code_list[code_list[base + 2]]
            code_list[code_list[base + 3]] = a * b
        i = i + 1
    return code_list


assert compute("99") == [99]
assert compute("1,0,0,0,99") == [2, 0, 0, 0, 99]
assert compute("1,1,1,4,99,5,6,0,99") == [30, 1, 1, 4, 2, 5, 6, 0, 99]

input_str = """1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,5,23,2,9,23,27,1,5,27,
31,1,5,31,35,1,35,13,39,1,39,9,43,1,5,43,47,1,47,6,51,1,51,13,55,1,55,9,59,1,59,
13,63,2,63,13,67,1,67,10,71,1,71,6,75,2,10,75,79,2,10,79,83,1,5,83,87,2,6,87,91,
1,91,6,95,1,95,13,99,2,99,13,103,1,103,9,107,1,10,107,111,2,111,13,115,1,10,115,
119,1,10,119,123,2,13,123,127,2,6,127,131,1,13,131,135,1,135,2,139,1,139,6,0,99,
2,0,14,0"""


for noun in range(99):
    for verb in range(99):
        if compute(input_str, noun, verb)[0] == 19690720:
            print(f"{noun} * {verb} = {100 * noun + verb}")
            break
