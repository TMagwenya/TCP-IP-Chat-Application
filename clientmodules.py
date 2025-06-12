import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from protocol import encode_message, decode_message  

APP_NAME = "TCP Chat App"
APP_TITLE_FONT = ("Arial", 16, "bold")

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title(APP_NAME)
        self.sock = None
        self.running = False
        self.client_name = tk.StringVar()
        self.msg_target_mode = tk.StringVar(value="Public")
        self.private_target = tk.StringVar()