#!/usr/bin/env python3
import socket
import struct
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import argparse

possible_hashes = ['sha1','sha512-224','sha512-256','sha224','sha256', 'sha384', 'sha512', 'sha3-224', 'sha3-256', 'sha3-384', 'sha3-512', 'shake128', 'shake256', 'md5', 'blake2b', 'blake2s']
hash_functions = [hashes.SHA1(), hashes.SHA512_224(),hashes.SHA512_256(), hashes.SHA224(), hashes.SHA256(), hashes.SHA384(), hashes.SHA512(), hashes.SHA3_224(), hashes.SHA3_256(), hashes.SHA3_384(), hashes.SHA3_512(), hashes.SHAKE128(128), hashes.SHAKE256(256), hashes.MD5(), hashes.BLAKE2b(64), hashes.BLAKE2s(32)]


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

localhost = "127.0.0.1"
port = 55841

def send_msg(sock, signature, msg, args):
    # Prefix each message with a 4-byte length (network byte order)
    #print(hashlib.md5(msg).hexdigest())
    msg = struct.pack('>I', len(msg)) + struct.pack('>Q', round(time.time()*1000)) + struct.pack('>I', possible_hashes.index(args.hash)) + struct.pack('>?', args.control) + struct.pack('>I', len(signature)) + signature + msg
    sock.sendall(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ha', '--hash', help='Input signature hash, like in \'sha256\' or \'md5\'', default='sha256')
    parser.add_argument('-l', '--loop', help='Input amount of times to loop', type=int, default=1)
    parser.add_argument('-c', '--control', help='Turn off digital signature', action="store_true")
    args = parser.parse_args()

    if(args.hash not in possible_hashes):
        print("Please Input a Valid Hash")
        exit(-1)

    pubkey_file = open('pubkey','w')#Publishes public key for reciever to see (local file for this setup)
    pubkey_file.write(public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8'))
    pubkey_file.close()

    for i in range(args.loop):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((localhost, port))

            data_file = open('credit_card.json')#gets the data from the file
            data = data_file.read()
            data_file.close()
            data = data.encode('utf-8')

            if args.control:
                send_msg(s, b"", data, args)
                s.close
                continue
            
            signature = private_key.sign(#creates signature
                data,
                padding.PSS(
                    mgf=padding.MGF1(hash_functions[possible_hashes.index(args.hash)]),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hash_functions[possible_hashes.index(args.hash)]
            )

            send_msg(s, signature, data, args)
            s.close()