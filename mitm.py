#!/usr/bin/env python3
import socket
import struct

localhost = "127.0.0.1"
portin = 55841
portout = 55842

def send_msg(sock, headers, hash_len, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)-hash_len) + headers + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]

    headers = recvall(sock, 17)
    hash_len = struct.unpack('>I', headers[13:17])[0]
    # Read the message data
    return headers, hash_len, recvall(sock, msglen + hash_len)

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
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socin:
        socin.bind((localhost, portin))
        socin.listen()#waits for incoming message
        while True:
            conn, addr = socin.accept()#accepts incoming connection
            headers, hash_len, data = recv_msg(conn)

            #EDIT DATA HERE

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socout:
                socout.connect((localhost, portout))
                send_msg(socout, headers, hash_len, data)
                socout.close()