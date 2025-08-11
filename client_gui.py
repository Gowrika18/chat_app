import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

# ---------------------------
# SERVER CONFIG
# ---------------------------
HOST = '127.0.0.1'
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ---------------------------
# EMOJI DICTIONARY
# ---------------------------
EMOJIS = {
    ":smile:": "😄",
    ":heart:": "❤",
    ":thumbsup:": "👍",
    ":laugh:": "😂",
    ":sad:": "😢"
}

# ---------------------------
# GUI FUNCTIONS
# ---------------------------
def connect_to_server():
    try:
        client.connect((HOST, PORT))
        if username.get().strip() == "":
            messagebox.showerror("Input Error", "Please enter a username.")
            return
        client.send(username.get().encode('utf-8'))
        login_window.destroy()
        open_chat_window()
    except Exception as e:
        messagebox.showerror("Connection Error", f"Unable to connect to server.\n{e}")

def open_chat_window():
    global chat_area, message_entry

    chat_window = tk.Tk()
    chat_window.title(f"Chat - {username.get()}")
    chat_window.geometry("500x500")

    chat_area = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, state='disabled', font=("Arial", 11))
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    message_frame = tk.Frame(chat_window)
    message_frame.pack(fill=tk.X, padx=10, pady=10)

    message_entry = tk.Entry(message_frame, font=("Arial", 11))
    message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    message_entry.focus()

    # Live emoji replacement while typing
    message_entry.bind("<KeyRelease>", replace_emojis_live)
    message_entry.bind("<Return>", lambda event: send_message())

    send_button = tk.Button(message_frame, text="Send", font=("Arial", 10), command=send_message)
    send_button.pack(side=tk.RIGHT)

    threading.Thread(target=receive_messages, daemon=True).start()
    chat_window.mainloop()

def replace_emojis_live(event=None):
    """Replace emoji codes with emojis as user types"""
    text = message_entry.get()
    for code, emoji in EMOJIS.items():
        if code in text:
            text = text.replace(code, emoji)
    # keep cursor at the end after replacement
    pos = message_entry.index(tk.INSERT)
    message_entry.delete(0, tk.END)
    message_entry.insert(0, text)
    message_entry.icursor(pos)

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            if message == "NICK":  # Ignore the nickname request from server
                continue
            display_message(message)
        except:
            messagebox.showerror("Error", "Disconnected from server.")
            try:
                client.close()
            except:
                pass
            break


def send_message():
    msg = message_entry.get()
    if msg.strip():
        timestamp = datetime.now().strftime("%H:%M")
        full_message = f"[{timestamp}] {username.get()}: {msg}"
        try:
            client.send(full_message.encode('utf-8'))
        except:
            messagebox.showerror("Error", "Message could not be sent.")
        message_entry.delete(0, tk.END)

def display_message(message):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, message + "\n")
    chat_area.config(state='disabled')
    chat_area.see(tk.END)

# ---------------------------
# LOGIN WINDOW
# ---------------------------
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")

tk.Label(login_window, text="Enter Username:", font=("Arial", 12)).pack(pady=10)
username = tk.StringVar()
username_entry = tk.Entry(login_window, textvariable=username, font=("Arial", 12))
username_entry.pack(pady=5)
username_entry.focus()

connect_button = tk.Button(login_window, text="Connect", font=("Arial", 11), command=connect_to_server)
connect_button.pack(pady=10)

login_window.mainloop()