import task6_task7
import math


def calculate_hash(n, IV, message):
    message_length = len(message)
    bin_message_length = bin(message_length).replace('0b', '')
    bin_message_length = bin_message_length.zfill(n)

    message_lis = []

    for i in range(math.ceil(len(message)/n)):
        mi = message[i*n:(i+1)*n]
        message_lis.append(mi)

    message_lis[-1] = message_lis[-1].zfill(n)
    message_lis.append(bin_message_length)

    hashed = ''

    for i in range(len(message_lis)):
        # print(IV + message_lis[i])
        hashed = task6_task7.calculate_hash(int(IV, 2), int(message_lis[i], 2))
        # print(hashed)
        IV = hashed

    return hashed


# n = int(input("Enter fixed hash length: "))
# IV = input("Enter Initialization Vector: ")
# message = input("Enter message: ")

# hash_output = calculate_hash(n, IV, message)
# print(hash_output, len(hash_output))

# print(message_lis)
