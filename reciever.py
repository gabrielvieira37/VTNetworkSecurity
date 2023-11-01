#!/usr/bin/env python3
import socket
import struct
import time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json
import decision_maker

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
    signature = recvall(sock, 256)
    # Read the message data
    return recvall(sock, msglen), msgtime, signature

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
            data, msgtime, signature= recv_msg(conn)
            time_in_transit = (round(time.time() * 1000) - msgtime)
            print("milliseconds in transit: " + str(time_in_transit))

            pubkey_file = open('pubkey')#get public key from file
            pubkey_data = pubkey_file.read()
            pubkey_file.close()
            pubkey = serialization.load_pem_public_key(pubkey_data.encode('utf-8'))

            data = bytes(data)
            signature = bytes(signature)
            try:#get signature verification with public key and data
                pubkey.verify(
                    signature,
                    data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
            except Exception as e:
                print("Invalid Signature or Hash")
                exit()
            print("Valid Signature and Hash")
            result_json = json.loads(data.decode('utf-8'))
            pruned_json = []
            for item in result_json:
                if 'Accuracy' in item.keys() and int(item['Accuracy']) == 1:
                    pruned_json.append(item)
            decision_maker.decision_maker(json.dumps(pruned_json))