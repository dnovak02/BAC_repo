#! /usr/bin/python3

import socket
import json
from CAF import CAF

def server_program():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket()  
    server_socket.bind((host, port))
    server_socket.listen(2)
    
    while True:
        connection_accepted = False
        if not connection_accepted:
            conn, address = server_socket.accept()
            connection_accepted = True
            CAF_object = CAF()
        while connection_accepted:
            data = conn.recv(1024).decode()
            if not data:
                connection_accepted = False
                break
            CAF_object.signal_Parsing(data)
            return_data = CAF_object.evaulate()
            conn.send(return_data.encode())

if __name__ == '__main__':
    server_program()