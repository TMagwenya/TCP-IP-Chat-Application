# server.py
import socket
import threading
from protocol import encode_message, decode_message

HOST = '0.0.0.0'
PORT = 12345

clients = []

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = decode_message(data)
            print(f"[{addr}] {message}")
            broadcast_message(message, client_socket)
    except (ConnectionResetError, ConnectionAbortedError):
        pass
    finally:
        print(f"[DISCONNECTED] {addr}")
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

def broadcast_message(message, sender_socket):
    data = encode_message(message)
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(data)
            except:
                pass

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server started on {HOST}:{PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
