g = 163
p = 37537


def l_func(x): return 2*x


def h_calc(input1, input2):
    part_a = bin(pow(g, int(input1, 2), p))
    part_a = part_a.replace('0b', '')
    part_a = part_a.zfill(16)

    final_bit = 0
    for i in range(len(input1)):
        final_bit ^= (int(input1[i]) & int(input2[i])) % 2
        # print(i, end=" ")

    # print(len(part_a), len(input2))
    return part_a + input2 + str(final_bit)


def g_calc(initial_seed):
    binary_string = initial_seed
    output = ''
    for i in range(l_func(len(initial_seed))):
        part1 = binary_string[:len(binary_string)//2]
        part2 = binary_string[len(binary_string)//2:]
        binary_string = h_calc(part1, part2)
        output += binary_string[-1]
        binary_string = binary_string[:-1]

    return output


# seed = input("Enter a seed: ")
# print(g_calc(seed))
