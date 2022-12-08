import socket
import json

def send_signal(client_socket,message):
    client_socket.send(message.encode())
    data_not_arrived = True
    while data_not_arrived:
        data = client_socket.recv(1024).decode()
        data_not_arrived = False
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