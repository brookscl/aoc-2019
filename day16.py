import math
import numpy
import time

PATTERN = [0, 1, 0, -1]
PATTERN_LENGTH = 4


def fft(signal, phases, extend=1):
    signal_length = len(signal)
    places_to_compute = signal_length * extend

    for phase in range(phases):
        output = ""
        signal_list = [int(d) for d in signal]
        for i in range(places_to_compute):
            # Instead of multiplying, let's add/subtract
            sum = 0
            j = i
            while j < signal_length * extend:
                for spread in range(i + 1):
                    if (j + spread) < (signal_length * extend):
                        sum += signal_list[(j + spread) % signal_length]
                j += 4 * (i + 1)

            # Move this inside loop above
            j = 3 * i + 2
            while j < signal_length * extend:
                for spread in range(i + 1):
                    if (j + spread) < (signal_length * extend):
                        sum -= signal_list[(j + spread) % signal_length]
                j += 4 * (i + 1)
            output += str(sum)[-1]
        signal = output
    return output[:8]


input_signal = "12345678"
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

with open("day16_input.txt") as f:
    content = f.readlines()

real_input_signal = content[0].strip()
start_time = time.time()
output_signal = fft(real_input_signal, 100)
print("--- %s seconds ---" % (time.time() - start_time))
assert output_signal == "94960436"
print(f"Output: {output_signal}")

# Part 2


def quick_fft(input_signal):
    offset = int(input_signal[:7])
    signal_list = [int(d) for d in input_signal]
    signal_list = signal_list * 10000
    signal_list = signal_list[offset:]

    phases = 100
    for phase in range(phases):
        output = []
        s = sum(signal_list)
        for i in range(len(signal_list)):

            output.append(int(str(s)[-1]))
            s -= signal_list[i]
        signal_list = output
        # print(f"Phase {phase} completed, signal: {signal_list[:8]}")
    return "".join(str(x) for x in signal_list[:8])


# 03036732577212944063491565474664 becomes 84462026


# The starting offset is barely smaller than the length of the signal


input_signal = "03036732577212944063491565474664"
output = quick_fft(input_signal)
assert output == "84462026"

input_signal = "02935109699940807407585447034323"
output = quick_fft(input_signal)
assert output == "78725270"

start_time = time.time()
output_signal = quick_fft(real_input_signal)
print("--- %s seconds ---" % (time.time() - start_time))
print(f"Output: {output_signal}")
