# server.py
import socket
import threading

# Server details
HOST = '127.0.0.1'  # Localhost (use your IP for LAN)
PORT = 55555        # Port number

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast message to all clients
def broadcast(message, sender=None):
    for client in clients:
        if client !=sender:
         client.send(message)

# Handle messages from a single client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, sender=client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat.'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Accept new clients
def receive():
    print(f"Server running on {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()