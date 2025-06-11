import socket
import threading
from protocol import encode_message, decode_message

HOST = 'localhost'
PORT = 12345

clients = {}  # socket: username

def handle_client(client_socket, addr):
    username = None
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = decode_message(data)

            # Handle registration
            if message.startswith("__register__"):
                _, username = message.split("|", 1)
                clients[client_socket] = username
                print(f"[REGISTERED] {addr} as {username}")
                continue

            sender, target, msg_text, time_sent = message.split("|")

            print(f"[{sender}] -> [{target}] : {msg_text}")

            if target == "All":
                broadcast_message(message, client_socket)
            else:
                send_private_message(message, target)
    except (ConnectionResetError, ConnectionAbortedError):
        pass
    finally:
        print(f"[DISCONNECTED] {addr}")
        if client_socket in clients:
            del clients[client_socket]
        client_socket.close()

def broadcast_message(message, sender_socket):
    data = encode_message(message)
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(data)
            except:
                pass