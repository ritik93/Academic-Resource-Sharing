import socket
import tqdm
import os
import getpass
import sys
import hashlib
import ssl
import time
import threading 

def client() :
    username = getpass.getuser()
    print("Username : " +username)

    password = "948fe603f61dc036b5c596dc09fe3ce3f3d30dc90f024c85f3c82db2ccab679d"       #hash generated by running password_hash.py

    pswd = getpass.getpass()
    test = (pswd).encode()
    pswd_in = str(hashlib.sha256(test).hexdigest())

    if pswd_in == password :
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        # create the client socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # the ip address or hostname of the server, the receiver
        host = socket.gethostbyname(socket.gethostname())
        #host = "10.35.70.9"
        # the port to be used
        port = 33333

        server_sni_hostname = 'example.com'
        server_cert = "server.crt"
        client_cert = "client.crt"
        client_key = "client.key"

        # Create an SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
        context.load_cert_chain(certfile=client_cert, keyfile=client_key)

        conn = context.wrap_socket(s, server_side = False, server_hostname = server_sni_hostname)
        print(f"[+] Connecting to {host}:{port}")
        conn.connect((host, port))
        print("[+] Connected to ", host)

        server_certificate = conn.getpeercert()
        subject = dict(item[0]for item in server_certificate['subject'])
        commonName = subject['commonName']

        if not server_certificate :
            raise Exception("Unable to retrieve server certificate")

        if commonName != 'example.com':
            raise Exception("Incorrect common name in server certificate")

        notAfterTimestamp   = ssl.cert_time_to_seconds(server_certificate['notAfter'])
        notBeforeTimestamp  = ssl.cert_time_to_seconds(server_certificate['notBefore'])
        currentTimeStamp    = time.time()

        if currentTimeStamp > notAfterTimestamp:
            raise Exception("Expired server certificate")
    
        if currentTimeStamp < notBeforeTimestamp:
            raise Exception("Server certificate not yet active")
        
        print("SSL established. Peer: {}".format(server_certificate))

        
        # the name of file we want to send
        filename = input("File to Transfer : ")

        # get the file size
        filesize = os.path.getsize(filename)

        # send the filename and filesize
        conn.send(f"{filename}{SEPARATOR}{filesize}".encode())

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
                conn.sendall(bytes_read)

                # update the progress bar
                progress.update(len(bytes_read))

        # close the socket
        conn.close()

    else : 
        sys.exit("Password Incorrect")
    
def server() :
    username = getpass.getuser()
    print("Username : " +username)

    password = "b3eacd33433b31b5252351032c9b3e7a2e7aa7738d5decdf0dd6c62680853c06"       #hash generated by running password_hash.py

    pswd = getpass.getpass()
    test = (pswd).encode()
    pswd_in = str(hashlib.sha256(test).hexdigest())

    if pswd_in == password :
        # create the server socket
        # TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # device's IP address
        #SERVER_HOST = "0.0.0.0"
        SERVER_HOST = socket.gethostbyname(socket.gethostname())
        SERVER_PORT = 33333

        # receive 4096 bytes each time
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"

        server_cert = "server.crt"
        server_key = "server.key"
        client_certs = "client.crt"

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(certfile=server_cert, keyfile=server_key)
        context.load_verify_locations(cafile=client_certs)

        # bind the socket to our local address
        s.bind((SERVER_HOST, SERVER_PORT))

        # enabling our server to accept connections
        # 10 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        s.listen(10)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

        def threading_clients(client_socket, address):
            print(f"[+] {address} is connected.")

            conn = context.wrap_socket(client_socket, server_side = True)

            client_certificate = conn.getpeercert()
            
            subject = dict(item[0] for item in client_certificate['subject'])
            commonName = subject['commonName']

            if not client_certificate :
                raise Exception("Unable to get the certificate from the client")

            if commonName != 'client' :
                raise Exception("Incorrect common name in client certificate")

            notAfterTimestamp   = ssl.cert_time_to_seconds(client_certificate['notAfter'])
            notBeforeTimestamp  = ssl.cert_time_to_seconds(client_certificate['notBefore'])
            currentTimeStamp    = time.time()

            if currentTimeStamp > notAfterTimestamp:
                raise Exception("Expired server certificate")
        
            if currentTimeStamp < notBeforeTimestamp:
                raise Exception("Server certificate not yet active")

            print("SSL established. Peer: {}".format(client_certificate))

            # receive the file infos
            # receive using client socket, not server socket
            received = conn.recv(BUFFER_SIZE).decode()
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
                    bytes_read = conn.recv(BUFFER_SIZE)
                    
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break

                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    
                    # update the progress bar
                    progress.update(len(bytes_read))

            # close the client socket
            conn.close()

        while (True) :
            client_socket, address = s.accept()
            thread = threading.Thread(target = threading_clients, args = (client_socket, address))
            thread.start()
            print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")
       
    else :
        sys.exit("Password Incorrect")

def main() :
    while 1 :
        inputstr = str(input("Do you want to act as a Server or a Client ?\nUsage :\nFor acting as a Server, enter  : SERVER\nFor acting as a Client, enter  : CLIENT\nFor exiting, enter : EXIT\n"))
        if inputstr == "SERVER" :
            server()
        elif inputstr == "CLIENT" :
            client()
        elif inputstr == "EXIT" :
            sys.exit("Program Exited\n")
        else :
            print("Incorrect Input\nSee Usage")

if __name__ == "__main__" :
    main()