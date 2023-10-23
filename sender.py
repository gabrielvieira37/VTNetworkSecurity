#!/usr/bin/env python3
import socket
import struct
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

localhost = "127.0.0.1"
port = 55841

def send_msg(sock, signature, msg):
    # Prefix each message with a 4-byte length (network byte order)
    #print(hashlib.md5(msg).hexdigest())
    msg = struct.pack('>I', len(msg)) + struct.pack('>Q', round(time.time()*1000)) + signature + msg
    sock.sendall(msg)

if __name__ == "__main__":

    #GENERATE DATA HERE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((localhost, port))
        pubkey_file = open('pubkey','w')#Publishes public key for reciever to see (local file for this setup)
        pubkey_file.write(public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8'))
        pubkey_file.close()

        data_file = open('credit_card.json')#gets the data from the file
        data = data_file.read()
        data_file.close()
        data = data.encode('utf-8')
        
        signature = private_key.sign(#creates signature
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        send_msg(s, signature, data)
        s.close()