import socket
import threading
import microservices.account as account
import microservices.transaction as transaction
import microservices.payment as payment
import json

HOST = "127.0.0.1"
PORT = 1234

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
            match data:
                case "1":
                    account_data = account.get_balance(current_client['id'])
                    json_account_data = json.dumps(account_data)
                    conn.sendall(json_account_data.encode())
                case "2":
                    info = conn.recv(1024).decode()
                    amount = float(info.split(";")[0])
                    destination = info.split(";")[1]
                    response = transaction.deposit(amount, destination, current_client["id"])
                    conn.send(response.encode())
                case "3":
                    info = conn.recv(1024).decode()
                    amount = float(info.split(";")[0])
                    bank_account = info.split(";")[1]
                    response = transaction.withdraw(amount, bank_account, current_client["id"])
                    conn.send(response.encode())
                case "4":
                    pass
                case "5":
                    pass
                case "6":
                    accounts = account.get_account_info(current_client["id"])
                    result = {
                        "name": current_client["name"],
                        "type": current_client["type"],
                        "accounts": accounts
                    }
                    json_result = json.dumps(result)
                    conn.sendall(json_result.encode())
        else:
            login_id = data.split(";")[0]
            login_pwd = data.split(";")[1]
            current_client = account.login(login_id, login_pwd)
            if (current_client['success']):
                logged_in = True
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