#!/usr/bin/env python3
import socket
import struct

localhost = "127.0.0.1"
port = 55842

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((localhost, port))
        s.listen()#waits for incoming message
        conn, addr = s.accept()#accepts incoming connection
        data = recv_msg(conn)
        s.close()
        print(data)#RECIEVED DATA HERE