import math
import numpy
import time

input_signal = "12345678"

PATTERN = [0, 1, 0, -1]
PATTERN_LENGTH = 4


def fft(signal, phases, extend=1):
    # extend pattern to be at least as long as signal
    signal_length = len(signal)
    # extend = math.ceil(len(signal) / len(PATTERN)) + 1
    # pattern = PATTERN * extend

    for phase in range(phases):
        output = ""
        signal_list = [int(d) for d in signal]
        for i in range(signal_length * extend):
            # Hmmm... pattern can be generated on the fly rather
            # than pre-building an array.
            # How long will pattern be zero at start? Can start
            # range there.

            # p = numpy.repeat(pattern, i + 1)[1 : signal_length + 1]
            # product = numpy.multiply(signal_list, p)
            # sum = numpy.sum(product)

            # Instead of multiplying, let's add/subtract
            sum = 0
            for j in range(i, signal_length * extend):
                p = PATTERN[(((j + 1) // (i + 1))) % PATTERN_LENGTH]
                if p == -1:
                    sum -= signal_list[j % signal_length]
                elif p == 1:
                    sum += signal_list[j % signal_length]
            output += str(sum)[-1]
        signal = output
    return output[:8]


def fft_with_offset(signal, phases, extend=1000):
    # extend pattern to be at least as long as signal
    signal = signal * extend
    signal_length = len(signal)
    offset = int(signal[:7])
    # extend = math.ceil(len(signal) / len(PATTERN)) + 1
    # pattern = PATTERN * extend

    for phase in range(phases):
        output = ""
        signal_list = [int(d) for d in signal]
        for i in range(signal_length):
            # Hmmm... pattern can be generated on the fly rather
            # than pre-building an array.
            # How long will pattern be zero at start? Can start
            # range there.

            # p = numpy.repeat(pattern, i + 1)[1 : signal_length + 1]
            # product = numpy.multiply(signal_list, p)
            # sum = numpy.sum(product)

            # Instead of multiplying, let's add/subtract
            sum = 0
            for j in range(i, signal_length * extend):
                p = PATTERN[(((j + 1) // (i + 1))) % PATTERN_LENGTH]
                if p == -1:
                    sum -= signal_list[j % signal_length]
                elif p == 1:
                    sum += signal_list[j % signal_length]
            output += str(sum)[-1]
        signal = output
        print(f"Phase {phase} completed, signal={signal}")
    return signal[offset : offset + 8]


def produce_output_with_offset(signal):
    offset = int(signal[:7])
    return signal[offset : offset + 8]


output_signal = fft(input_signal, 1)
assert output_signal == "48226158"

output_signal = fft(input_signal, 2)
assert output_signal == "34040438"

output_signal = fft(input_signal, 4)
assert output_signal == "01029498"


input_signal = "80871224585914546619083218645595"
output_signal = fft(input_signal, 100)
assert output_signal == "24176176"

# Part 1

# with open("day16_input.txt") as f:
#     content = f.readlines()

# real_input_signal = content[0].strip()
# start_time = time.time()
# output_signal = fft(real_input_signal, 100)
# print("--- %s seconds ---" % (time.time() - start_time))
# assert output_signal == "94960436"
# print(f"Output: {output_signal}")

# Part 2
input_signal = "03036732577212944063491565474664"
output = fft_with_offset(input_signal, 100, 10000)
assert output == "84462026"
