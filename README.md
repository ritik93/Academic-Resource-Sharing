# Academic-Resource-Sharing
Creating a Peer-to-Peer Academic Resource Sharing System

## Implementation

1. Two Peers are created, namely, Peer A and Peer B
2. On running both peerA.py and peerB.py it is asked that whether you want to act as a client or a server
3. When one peer acts a client and the other as a server
4. The client can then start sending the file to the server
5. peerA.py and peerB.py run infinitely until the user explicitly enters "EXIT"

## How to Run the code on your machine :
1. Install tqdm using the command : pip3 install tqdm (For Mac) or pip install tqdm (For Windows)
2. Run the file peerA.py on a terminal window run the following command :
   For Mac :                             For Windows :
   python3 peerA.py                      python peerA.py
3. Run the file peerB.py on a second terminal window
   For Mac :                             For Windows :
   python3 peerB.py                      python peerB.py
4. If you choose to run the peer as a SERVER, the password is : server
5. If you choose to run the peer as a CLIENT, the password is : client
6. Enter the filepath on the client side
7. After the file is transferred, the code starts again from step 4
8. If the peer wishes to exit, enter : EXIT
