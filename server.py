import socket
import threading
import microservices.account as account
import json

HOST = "127.0.0.1"
PORT = 55555

def handle_client(conn, addr):
    print(f"Client connected: {addr}")

    current_client = {}
    logged_in = False

    while True:
        data = conn.recv(1024)
        if not data:
            print(f"Client disconnected: {addr}")
            break
        data = data.decode()
        if logged_in:
            match data['choice']:
                case "1":
                    print(current_client)
                    account_data = account.get_balance(current_client['id'])
                    json_account_data = json.dumps(account_data)
                    conn.sendall(json_account_data.encode())
        else:
            login_id = data.split(";")[0]
            login_pwd = data.split(";")[1]
            current_client = account.login(login_id, login_pwd)
            if (current_client['success']):
                conn.send('proceed'.encode())

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