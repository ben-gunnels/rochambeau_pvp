import socket
import struct
import threading
from lib.MessagePasser import MessagePasser

HOST = '127.0.0.1'  # Change to server IP for remote testing
PORT = 5555

messenger = MessagePasser()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

client.connect((HOST, PORT))

# Receive initial message from server
print(client.recv(1024).decode())

def message_listener():
    while True:
        msg = input()

        if not msg:
            continue

        messenger.send_message(client, msg + "\n")


# threading.Thread(target=messenger.receive_message, args=(client, ), daemon=True).start()

def listen():
    isListening = 1
    sendThread = threading.Thread(target=message_listener, daemon=True).start()

    while isListening:
        try: 
            msg = messenger.receive_message(client)
        except:
            continue
        try:
            print(msg)
        except Exception as p:
            pass

if __name__ == "__main__":
    listen()
    
    
