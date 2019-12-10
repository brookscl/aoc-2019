

def find_zero_layer(image, layer_size):
    layers = [image[i: i + layer_size] for i in range(0, len(image), layer_size)]
    check_zeros = {}
    for layer in layers:
        check_zero = layer.count('0')
        check_ones_twos = layer.count('1') * layer.count('2')
        check_zeros[check_ones_twos] = check_zero

    return min(check_zeros, key=check_zeros.get)


test_image = "123456789012"

layer_size = 6

# assert find_zero_layer(test_image, layer_size) == 1

# Part 1

with open("day08_image.txt") as f:
    content = f.readlines()

image = content[0].strip()
print(find_zero_layer(image, 150))


# Part 2

def collapse(image, width, height):
    final_image = [['2' for x in range(width)] for x in range(height)]
    layer_size = width * height
    layers = [image[i: i + layer_size] for i in range(0, len(image), layer_size)]
    for layer in layers:
        for row in range(height):
            for col in range(width):
                if final_image[row][col] == '2':
                    final_image[row][col] = layer[row * width + col]

    return final_image


def render(image, width, height):
    for row in range(height):
        for col in range(width):
            pixel = image[row][col]
            if pixel == '0':
                print('   ', end='')
            else:
                print(' * ', end='')
        print('  ', flush=True)

# render("0222112222120000", 2, 2)


width = 25
height = 6

final = collapse(image, width, height)

render(final, width, height)
