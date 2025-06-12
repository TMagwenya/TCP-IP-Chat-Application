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

        #  Appearance 
        self.bg_color = "#f0f0f0"
        self.text_color = "#000000"
        self.button_color = "#4CAF50"
        self.font = ("Arial", 12)
        # 

        self.master.configure(bg=self.bg_color)