
def find_zero_layer(image, layer_size):
    layers = [image[i:i+layer_size] for i in range(0, len(image), layer_size)]
    check_zeros = {}
    for layer in layers:
        check_zero = layer.count('0')
        check_ones_twos = layer.count('1') * layer.count('2')
        check_zeros[check_ones_twos] = check_zero

    return min(check_zeros, key=check_zeros.get)

test_image = "123456789012"

layer_size = 6

# assert find_zero_layer(test_image, layer_size) == 1


with open("day08_image.txt") as f:
    content = f.readlines()

image = content[0].strip()
print(find_zero_layer(image, 150))
