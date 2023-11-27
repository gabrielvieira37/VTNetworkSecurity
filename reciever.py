#!/usr/bin/env python3
import socket
import struct
import time
import os
import pandas as pd
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json
import decision_maker

localhost = "127.0.0.1"
port = 55842
possible_hashes = ['sha1','sha512-224','sha512-256','sha224','sha256', 'sha384', 'sha512', 'sha3-224', 'sha3-256', 'sha3-384', 'sha3-512', 'shake128', 'shake256', 'md5', 'blake2b', 'blake2s']
hash_functions = [hashes.SHA1(), hashes.SHA512_224(),hashes.SHA512_256(), hashes.SHA224(), hashes.SHA256(), hashes.SHA384(), hashes.SHA512(), hashes.SHA3_224(), hashes.SHA3_256(), hashes.SHA3_384(), hashes.SHA3_512(), hashes.SHAKE128(128), hashes.SHAKE256(256), hashes.MD5(), hashes.BLAKE2b(64), hashes.BLAKE2s(32)]

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    raw_msgtime = recvall(sock, 8)
    msgtime = struct.unpack('>Q', raw_msgtime)[0]
    raw_hash_type = recvall(sock, 4)
    hash_type = struct.unpack('>I', raw_hash_type)[0]
    raw_control = recvall(sock, 1)
    control = struct.unpack('>?', raw_control)[0]
    raw_sig_len = recvall(sock, 4)
    sig_len = struct.unpack('>I', raw_sig_len)[0]
    signature = recvall(sock, sig_len)
    # Read the message data
    return recvall(sock, msglen), msgtime, signature, hash_type, control

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
            data, msgtime, signature, hash_type, control= recv_msg(conn)
            time_in_transit = (round(time.time() * 1000) - msgtime)
            print("milliseconds in transit: " + str(time_in_transit))

            time_file = f'received_times_{possible_hashes[hash_type].upper()}.json'
            if os.path.isfile(time_file):
                time_series = pd.read_json(time_file, typ='series')
                new_time_series = pd.Series([time_in_transit])
                final_time_series = pd.concat([time_series, new_time_series], ignore_index=True)
                final_time_series.to_json(time_file)
            else:    
                time_series = pd.Series([time_in_transit])
                time_series.to_json(time_file)

            pubkey_file = open('pubkey')#get public key from file
            pubkey_data = pubkey_file.read()
            pubkey_file.close()
            pubkey = serialization.load_pem_public_key(pubkey_data.encode('utf-8'))

            if not control:
                data = bytes(data)
                signature = bytes(signature)
                try:#get signature verification with public key and data
                    pubkey.verify(
                        signature,
                        data,
                        padding.PSS(
                            mgf=padding.MGF1(hash_functions[hash_type]),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hash_functions[hash_type]
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