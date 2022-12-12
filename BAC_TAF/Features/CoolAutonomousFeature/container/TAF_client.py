import socket
import json
import time

def send_signal(client_socket,message):
    client_socket.send(message.encode())
    time.sleep(0.5)
    data = client_socket.recv(1024).decode()
    return data

def client_program(json_signal):
    host = '127.0.0.1'
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))
    if(type(json_signal) == list):
        for signal in json_signal:
            signal = json.dumps(signal)
            data = send_signal(client_socket,signal)
    else:
        json_signal = json.dumps(json_signal)
        data = send_signal(client_socket,json_signal)
    client_socket.close()
    return data

if __name__ == '__main__':
    client_program()