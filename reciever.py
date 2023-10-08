#!/usr/bin/env python3
import socket
import struct
import time
import hashlib

localhost = "127.0.0.1"
port = 55842

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    raw_msgtime = recvall(sock, 8)
    msgtime = struct.unpack('>Q', raw_msgtime)[0]
    checksum = recvall(sock, 32)
    # Read the message data
    return recvall(sock, msglen), msgtime, checksum

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
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((localhost, port))
        s.listen()#waits for incoming message
        while True:
            conn, addr = s.accept()#accepts incoming connection
            data, msgtime, checksum = recv_msg(conn)
            time_in_transit = (round(time.time() * 1000) - msgtime)
            print("milliseconds in transit: " + str(time_in_transit))
            if bytes(hashlib.md5(data).hexdigest(), 'utf-8') == checksum:
                print("Checksum Matched")
            else:
                print("Checksums Did Not Match")
            #print(data)#RECIEVED DATA HERE