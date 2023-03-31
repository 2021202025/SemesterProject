import os
import socket


def pre_command(host):
    print("")
    print("Server running at @ ", host)
    print("")
    print("Waiting for a connection...")


def post_command():
    print("")
    # conn.recv(1024)
    print("Command sent, waiting for execution...")
    print("")


def pwd(command):
    try:
        conn.send(command.encode())
        post_command()
        files = conn.recv(5000)
        files = files.decode()
        print("Command output: ", files)
    except:
        return -1


def custom_dir(command):
    try:
        conn.send(command.encode())
        print("")
        dir_path = input("Custom dir: ")
        conn.send(dir_path.encode())
        post_command()
        files = conn.recv(5000)
        files = files.decode()
        print("Command output: ", files)
    except:
        return -1


def download_files(command):
    try:
        # FlushListen(conn)
        conn.send(command.encode())
        print("")
        filename = input("Filename/Path: ")
        conn.send(filename.encode())
        post_command()

        new_filename = input("New Filename: ")
        newfile = open(new_filename, "wb")

        count = 0
        conn.settimeout(5)
        while True:

            print("Downloading part->", count)

            try:
                data = conn.recv(1024)
            except:
                break
            count += 1

            if not data:
                break

            newfile.write(data)

        newfile.close()
        print("File downloaded successfully")
        print("")
    except:
        return -1


def remove_file(command):
    try:
        conn.send(command.encode())
        filepath = input("Filepath: ")
        conn.send(filepath.encode())
        post_command()
    except:
        return -1


def send_files(command):
    try:
        conn.send(command.encode())
        filename = input("New Filename: ")
        conn.send(filename.encode())
        filepath = input("Filepath: ")
        file = open(filepath, "rb")
        data = file.read(90000000)
        conn.send(data)
        post_command()
    except:
        return -1


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
host = socket.gethostname()
# host = "127.0.0.1"
port = 8080

s.bind((host, port))

pre_command(host)
s.listen(1)
conn, addr = s.accept()
print(addr, "has connected to the server successfully", end="\n\n")
conn.settimeout(5)

while True:
    command = input("Enter command: ")

    if command == "pwd":
        if(pwd(command) == -1):
            print("Command failed")
            print("")
            continue

    elif command == "ls":
        if(custom_dir(command) == -1):
            print("Command failed")
            print("")

    elif command == "download":
        if(download_files(command) == -1):
            print("Command failed")
            print("")

    elif command == "remove":
        if(remove_file(command) == -1):
            print("Command failed")
            print("")

    elif command == "send":
        if(send_files(command) == -1):
            print("Command failed")
            print("")

    elif command == "exit":
        conn.send(command.encode())
        break

    else:
        print("Command not recognized")
