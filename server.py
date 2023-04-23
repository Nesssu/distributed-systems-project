import socket
import threading

HOST = "127.0.0.1"
PORT = 55555

def handle_client(conn, addr):
    print(f"Client connected: {addr}")

    logged_in = False
    
    data = conn.recv(1024).decode()
    while True:
        if not data:
            print(f"Client disconnected: {addr}")
            break
        
        if logged_in:
            pass
        else:
            # Send the log in data to the microservice

            # If the log in data is valid, log in
            logged_in = True
            conn.send("proceed".encode())

    conn.close()
    return None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()