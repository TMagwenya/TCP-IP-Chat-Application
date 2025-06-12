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

        # App Title 
        self.title_label = tk.Label(master, text=APP_NAME, font=APP_TITLE_FONT, bg=self.bg_color, fg=self.text_color)
        self.title_label.pack(pady=(10, 5))

        #  Connect/Disconnect Buttons 
        
        top_button_frame = tk.Frame(master, bg=self.bg_color)
        top_button_frame.pack(pady=5)
        self.connect_button = tk.Button(top_button_frame, text="Connect", command=self.connect_to_server, bg=self.button_color, fg='white', font=self.font)
        self.connect_button.pack(side='left', padx=5)
        self.disconnect_button = tk.Button(top_button_frame, text="Disconnect", command=self.disconnect_from_server, bg=self.button_color, fg='white', font=self.font)
        self.disconnect_button.pack(side='left', padx=5)

        #  Username Entry 
        name_frame = tk.Frame(master, bg=self.bg_color)
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Username:", font=self.font, bg=self.bg_color).pack(side='left')
        self.username_entry = tk.Entry(name_frame, textvariable=self.client_name, font=self.font, width=20)
        self.username_entry.pack(side='left', padx=5)

        #  Mode Selection 
        mode_frame = tk.Frame(master, bg=self.bg_color)
        mode_frame.pack(pady=5)
        tk.Label(mode_frame, text="Message Mode:", font=self.font, bg=self.bg_color).pack(side='left')
        mode_menu = tk.OptionMenu(mode_frame, self.msg_target_mode, "Public", "Private", command=self.toggle_private_target)
        mode_menu.config(font=self.font)
        mode_menu.pack(side='left', padx=5)

        #  Private Target Input 
        self.private_frame = tk.Frame(master, bg=self.bg_color)
        tk.Label(self.private_frame, text="Target Username:", font=self.font, bg=self.bg_color).pack(side='left')
        self.private_entry = tk.Entry(self.private_frame, textvariable=self.private_target, font=self.font, width=20)
        self.private_entry.pack(side='left', padx=5)

        #  Chat Area 
        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20, bg=self.bg_color, fg=self.text_color, font=self.font)
        self.chat_area.pack(padx=10, pady=10)

        #  Message Entry + Send Button 
        
        bottom_frame = tk.Frame(master, bg=self.bg_color)
        bottom_frame.pack(pady=5)
        self.entry_msg = tk.Entry(bottom_frame, width=45, font=self.font)
        self.entry_msg.pack(side='left', padx=5)
        self.send_button = tk.Button(bottom_frame, text="Send", command=self.send_message, bg=self.button_color, fg='white', font=self.font, width=10)
        self.send_button.pack(side='left')

    def toggle_private_target(self, *args):
        if self.msg_target_mode.get() == "Private":
            self.private_frame.pack(pady=5)
        else:
            self.private_frame.forget()

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('localhost', 12345))
            self.running = True
            # Send your username to server
            self.sock.sendall(encode_message(f"__register__|{self.client_name.get()}"))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.append_chat("System", f"Connected to server as {self.client_name.get()}.")
        except Exception as e:
            self.append_chat("System", f"Connection failed: {e}")

    def disconnect_from_server(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.append_chat("System", "Disconnected from server.")

    def send_message(self):
        message = self.entry_msg.get()
        if message and self.sock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            mode = self.msg_target_mode.get()
            if mode == "Private":
                target = self.private_target.get().strip()
                if not target:
                    self.append_chat("System", "Please enter a target username for private message.")
                    return
            else:
                target = "All"
            full_message = f"{self.client_name.get()}|{target}|{message}|{timestamp}"
            try:
                self.sock.sendall(encode_message(full_message))
                self.append_chat("You", message, timestamp)
                self.entry_msg.delete(0, tk.END)
            except Exception as e:
                self.append_chat("System", f"Failed to send: {e}")

    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                message = decode_message(data)
                sender, _, msg_text, time_sent = message.split("|")
                display_name = "You" if sender == self.client_name.get() else sender
                self.append_chat(display_name, msg_text, time_sent)
            except:
                break
        self.disconnect_from_server()

    def append_chat(self, sender, message, timestamp=None):
        self.chat_area.configure(state='normal')
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_area.insert(tk.END, f"\n{timestamp}\n{sender}: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
