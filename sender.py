#!/usr/bin/env python3
import socket
import struct

localhost = "127.0.0.1"
port = 55841

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

if __name__ == "__main__":

    #GENERATE DATA HERE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((localhost, port))
        data = b"this is the data being sent"
        send_msg(s, data)