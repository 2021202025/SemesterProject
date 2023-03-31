import math
import random
import string
import prg


def computeGCD(x, y):
    while(y):
        x, y = y, x % y
    return x


# e needs to be co prime with N and Phi_N
def get_encryption_key(N, phi_N):
    possible_e = []
    for i in range(1, N+1):
        if (1 < i) and (i < phi_N):
            gcd = computeGCD(i, N)
            gcd_phi = computeGCD(i, phi_N)
            if (gcd == 1) and (gcd_phi == 1):
                # return i
                possible_e.append(i)
    if len(possible_e) > 1:
        return possible_e[random.randint(1, len(possible_e)-1)]
    else:
        return possible_e[0]


# choose d such that d*e mod phi_N = 1
def get_decryption_key(e, phi_N):
    possible_d = []
    for i in range(e * 25):
        if (e * i) % phi_N == 1:
            possible_d.append(i)
    if len(possible_d) > 1:
        return possible_d[random.randint(1, len(possible_d)-1)]
    else:
        return possible_d[0]
    # return possible_d[random.randint(1, len(possible_d) - 1)]


def text_to_digits(message):
    pool = string.ascii_letters + string.punctuation + " "
    # print(pool)
    # print(message)
    M = []
    ascii_values = []
    for character in message:
        # print(character)
        ascii_values.append(ord(character))

    # print(ascii_values)
    # print(ascii_values)
    # print(res)
    return ascii_values


def digits_to_text(message_digest):
    res = ''.join(chr(i) for i in message_digest)

    return res


def encrypt(M, public_key):
    return [(i ** public_key[0]) % public_key[1] for i in M]


def decrypt(CT, private_key):
    return [((i ** private_key[0]) % private_key[1]) for i in CT]


def message_to_binary(message_lis):
    binary_message = ""
    for i in message_lis:
        binary_message += bin(i).replace('0b', '').zfill(32)
    # print(len(binary_message))
    return binary_message


def message_to_binary8bit(message_lis):
    binary_message = ""
    for i in message_lis:
        binary_message += bin(i).replace('0b', '').zfill(8)
    # print(len(binary_message))
    return binary_message


def pad_rsa(fixed_bytes, binary_r, null_byte, binary_message):
    return fixed_bytes + binary_r + null_byte + binary_message


def remove_pad_rsa(cipher_text):
    message_lis = []
    n = len(cipher_text)//8
    for i in range(n):
        message_lis.append(int(cipher_text[i*8:i*8+8], 2))

    # print(message_lis)
    count = 0
    for i in message_lis:
        count += 1
        # print(count)
        if i == 0:
            break

    message_lis = message_lis[count:]
    encrypted_binary = message_to_binary8bit(message_lis)
    # print(encrypted_binary)

    message_lis = []
    n = len(encrypted_binary)//32
    # print(len(encrypted_binary))
    for i in range(n):
        # print(i)
        message_lis.append(int(encrypted_binary[i*32:i*32+32], 2))

    # print(message_lis)
    return message_lis


def encrypt_rsa(message):
    null_byte = "00000000"

    # print(prg.g_calc("011111001000111101001011000100011111100010011011"))
    fixed_bytes = "0101001111011010"
    binary_r = "0101001111011010011111001000111101001011000100011111100010011011"
    # binary_r = message_to_binary(r)
    # print(len(binary_r))
    # message length should be less than 1014 bytes

    parsed_message = text_to_digits(message)
    cipher_text = encrypt(parsed_message, public_key)
    # print()
    # print(cipher_text)
    binary_cipher = message_to_binary8bit(cipher_text)
    cipher_to_send = pad_rsa(fixed_bytes, binary_r, null_byte, binary_cipher)
    # decrypt_rsa(cipher_to_send)
    return cipher_to_send


def decrypt_rsa(received_cipher):
    pad_removed_cipher = remove_pad_rsa(received_cipher)
    # print(cipher_text)
    decrypted_text = decrypt(pad_removed_cipher, private_key)
    decrypted_message = digits_to_text(decrypted_text)
    # print(decrypted_message)
    return decrypted_message


p = 41
q = 59

# Public key N,e
N = p * q
phi_N = (p - 1) * (q - 1)
# print(N)
# print(phi_N)
e = get_encryption_key(N, phi_N)
# print(e)
d = get_decryption_key(e, phi_N)
# print(d)

while d == e:
    d = get_decryption_key(e, phi_N)

public_key = [e, N]
private_key = [d, N]
