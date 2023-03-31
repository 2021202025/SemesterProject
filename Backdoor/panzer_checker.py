import sys
import os
import task6_task7
import task7
import math
import requests
import colorama
from colorama import Fore, Back, Style

colorama.init()


def check_integrity():
    if getattr(sys, 'frozen', False):
        dir_path = os.path.dirname(sys.executable)
        os.chdir(dir_path)
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))

    # print(dir_path)

    pyfile = ""
    for root, dirs, files in os.walk(dir_path):
        for file in files:

            if file.endswith('panzer.py'):
                pyfile = os.path.join(root, file)
                # print(root+'/'+str(file))

    # print(pyfile)
    check = "panzer.py"

    f = open(pyfile, "r+")

    test_str = f.read()

    # printing original string
    # print("The original string is : " + str(test_str))

    # using join() + bytearray() + format()
    # Converting String to binary
    res = ''.join(format(i, '08b')
                  for i in bytearray(test_str, encoding='utf-8'))
    res = str(res)

    # printing result
    # print("The string after binary conversion : " + str(res))

    # n = int(input("Enter fixed hash length: "))
    # IV = input("Enter Initialization Vector: ")

    n = 64
    IV = "1010111110101111101011111010111110101111101011111010111110101111"
    binary_hash = task7.calculate_hash(n, IV, res)
    # print(hash)
    hex_hash = hex(int(binary_hash, 2))

    # print(binary_hash)
    # print(hex_hash)

    # sp=r&st=2022-02-22T16:29:17Z&se=2022-07-31T00:29:17Z&sv=2020-08-04&sr=b&sig=04HxsQrrTS1rwJeUX2Gjzv0U2XnE%2BfWP38VTCUfgDDw%3D
    # https://snsmanu.blob.core.windows.net/sns/Key.txt?sp=r&st=2022-02-22T16:29:17Z&se=2022-07-31T00:29:17Z&sv=2020-08-04&sr=b&sig=04HxsQrrTS1rwJeUX2Gjzv0U2XnE%2BfWP38VTCUfgDDw%3D
    r = requests.get("https://snsproject.blob.core.windows.net/snsproject/Key.txt?sp=r&st=2022-10-26T17:48:10Z&se=2023-10-31T01:48:10Z&sv=2021-06-08&sr=b&sig=kNEWqY879tBTGosxDFf0u68dwji%2FXAhC2T9uqs%2FCnvQ%3D")
    hashes = r.text.split("\n")

    # print(hashes)
    # print(hashes[0])
    # print(binary_hash)

    retrieved_binary_hash = hashes[0][:-1]
    retrieved_hex_hash = hashes[-1]

    if binary_hash == retrieved_binary_hash:
        if hex_hash == retrieved_hex_hash:
            # print('\033[1;92m' + "Hash is correct")
            return 1
        else:
            # print('\033[1;91m' + "Hash is incorrect")
            return 0
    else:
        # print('\033[1;91m' + "Hash is incorrect")
        return 0
    # print(hashes[0])
    # print(hashes[-1])


response = check_integrity()
if response == 1:
    print('\033[1;92m' + "Hash is correct")
    import panzer
    # panzer.game_intro()
    # panzer.gameLoop()
else:
    print('\033[1;91m' + "Hash is incorrect")
    print('\033[1;91m' + "Game files are corrupted, please redownload the game")
# check_integrity()
