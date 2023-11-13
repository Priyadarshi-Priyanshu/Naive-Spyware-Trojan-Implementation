import socket
import pickle
import threading

HEADER = 64
PORT = 5050
PUBLIC_IP = "192.168.29.202"
SERVER = socket.gethostbyname(PUBLIC_IP)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Receive the length of the pickled data
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    # Receive the pickled data
    serialized_data = conn.recv(msg_length)
    credentials = pickle.loads(serialized_data)

    # Extract username and password
    username = credentials['username']
    password = credentials['password']

    # Write username and password to a text file
    with open('credentials.txt', 'a') as file:
        file.write(f"Username: {username}, Password: {password}\n")

    print(f"[{addr}] Username: {username}, Password: {password}")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

        
start()