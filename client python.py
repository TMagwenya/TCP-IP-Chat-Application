# client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from protocol import encode_message, decode_message

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("TCP Chat Client")
        self.sock = None
        self.running = False

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=15)
        self.chat_area.pack(padx=10, pady=10)

        # Entry for message
        self.entry_msg = tk.Entry(master, width=40)
        self.entry_msg.pack(padx=10, pady=5, side='left')

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=5, pady=5, side='left')

        # Connect button
        self.connect_button = tk.Button(master, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(padx=5, pady=5, side='left')

        # Disconnect button
        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect_from_server)
        self.disconnect_button.pack(padx=5, pady=5, side='left')

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('127.0.0.1', 12345))
            self.running = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.append_chat("Connected to server.\n")
        except Exception as e:
            self.append_chat(f"Connection failed: {e}\n")

    def disconnect_from_server(self):
        self.running = False
        if self.sock:
            self.sock.close()
            self.append_chat("Disconnected from server.\n")

    def send_message(self):
        message = self.entry_msg.get()
        if message and self.sock:
            try:
                self.sock.sendall(encode_message(message))
                self.append_chat(f"You: {message}\n")
                self.entry_msg.delete(0, tk.END)
            except Exception as e:
                self.append_chat(f"Failed to send: {e}\n")

    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                message = decode_message(data)
                self.append_chat(f"Server: {message}\n")
            except:
                break
        self.disconnect_from_server()

    def append_chat(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message)
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()