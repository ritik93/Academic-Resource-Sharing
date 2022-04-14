# Generalised File Sharing
Created a secure File Sharing System where the multithreaded server listens for multiple clients 

## Implementation
1. Three Peers are created, namely, Peer A, Peer B and Peer C 
2. On running both peerA.py, peerB.py, peerC.py it is asked that whether you want to act as a client or a server
3. When one peer chooses to acts as a server, the other two peers can act as clients and connect to the server
4. The clients can then start sending the files to the server
5. The clients can run infinitely until the user explicitly enters "EXIT" and the multithreaded server will continue to listen for the clients 

## How to Run the code on remote rasberry pis and your local machine :
The steps are the same for running the files on your local machine except, the files to be run to run on you local machine are placed in a separate folder called Run_on_local and these are the following deifferences between the two files are as follows :  
  
In the python files (peerA.py, peerB.py, peerC.py) of Run_on_local :  
The host ip is retrieved using socket.gethostbyname() function  
  
In the python files (peerA.py, peerB.py, peerC.py) placed outside Run_on local which are to be run on remote rasberry pis :  
The host ip is explicity mentioned as "10.35.70.9" which had to be done so that a client program running on one rasberry pi can connect to another rasberry pi running a server program  
  
1. Install tqdm using the command :   
    For Mac and rasberry pi : pip3 install tqdm  
    For Windows : pip install tqdm
2. Run the file peerA.py on a terminal window run the following command :  
    For Mac and rasberry pi : python3 peerA.py  
    For Windows : python peerA.py
3. Run the file peerB.py on a second terminal window  
    For Mac and rasberry pi : python3 peerB.py                              
    For Windows : python peerC.py
4. Run the file peerC.py on a third terminal window  
    For Mac and rasberry pi : python3 peerC.py                              
    For Windows : python peerC.py
5. If you choose to run the peer as a SERVER, the password is : server
6. If you choose to run the peer as a CLIENT, the password is : client
7. Enter the filepath on the client side
8. After the file is transferred, the client starts again from step 5  
9. If the client wishes to exit, enter : EXIT
10. The multithreaded server will keep on running and listening for clients to connect
