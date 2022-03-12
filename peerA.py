import socket
import tqdm
import os
import getpass
import sys

def client() :
    username = getpass.getuser()
    print("Username : " +username)
    password = "password"
    pswd = getpass.getpass()

    if pswd == password :
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        # create the client socket
        s = socket.socket()

        # the ip address or hostname of the server, the receiver
        host = "10.6.9.187"

        # the port to be used
        port = 5001

        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected to ", host)

        # the name of file we want to send
        filename = input("File to Transfer : ")

        # get the file size
        filesize = os.path.getsize(filename)

        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:

                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break

                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)

                # update the progress bar
                progress.update(len(bytes_read))

        # close the socket
        s.close()

    else : 
        sys.exit("Password Incorrect")

def server() :
    username = getpass.getuser()
    print("Username : " +username)
    password = "password"
    pswd = getpass.getpass()

    if pswd == password :
        # device's IP address
        SERVER_HOST = "0.0.0.0"
        SERVER_PORT = 5001

        # receive 4096 bytes each time
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"

        # create the server socket
        # TCP socket
        s = socket.socket()

        # bind the socket to our local address
        s.bind((SERVER_HOST, SERVER_PORT))

        # enabling our server to accept connections
        # 10 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        s.listen(10)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

        # accept connection if there is any
        client_socket, address = s.accept() 
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")

        # receive the file infos
        # receive using client socket, not server socket
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)

        # remove absolute path if there is
        filename = os.path.basename(filename)

        # convert to integer
        filesize = int(filesize)

        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f: 
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break

                # write to the file the bytes we just received
                f.write(bytes_read)
                
                # update the progress bar
                progress.update(len(bytes_read))

        # close the client socket
        client_socket.close()

        # close the server socket
        s.close()

    else :
        sys.exit("Password Incorrect")

def main() :
    inputstr = str(input("Do you want to act as a Server or a Client ?\nUsage :\nFor acting as a Server, enter  : SERVER\nFor acting as a Client, enter  : CLIENT\n"))
    if inputstr == "SERVER" :
        server()
    elif inputstr == "CLIENT" :
        client()
    else :
        sys.exit("Incorrect Input\nSee Usage")

if __name__ == "__main__" :
    main()