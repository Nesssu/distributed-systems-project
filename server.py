import socket
import threading
import microservices.account as account
import microservices.transaction as transaction
import microservices.payment as payment
import json

HOST = "127.0.0.1"
PORT = 1234

def client_options(conn, current_client, data):
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
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            amount = float(info_split[0])
            bank_account = info_split[1]
            destination = info_split[2]
            response = transaction.transfer(amount, destination, bank_account, current_client["id"])
            conn.send(response.encode())
        case "5":
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            amount = float(info_split[0])
            bank_account = info_split[1]
            destination = info_split[2]
            response = payment.pay(amount, destination, bank_account, current_client["id"])
            conn.send(response.encode())
        case "6":
            accounts = account.get_account_info(current_client["id"])
            result = {
                "name": current_client["name"],
                "type": current_client["type"],
                "accounts": accounts
            }
            json_result = json.dumps(result)
            conn.sendall(json_result.encode())
    return None

def admin_options(conn, data):
    match data:
        case "1":
            clients = account.get_all_clients()
            json_clients = json.dumps(clients)
            conn.sendall(json_clients.encode())

        case "2":
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            name = info_split[0]
            password = info_split[1]
            response = account.create_client(name, password)
            conn.send(response.encode())

        case "3":
            client_id = conn.recv(1024).decode()
            response = account.delete_client(client_id)
            conn.send(response.encode())

        case "4":
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            client_id = info_split[0]
            account_type = info_split[1]
            response = account.create_account(client_id, account_type)
            conn.send(response.encode())

        case "5":
            account_id = conn.recv(1024).decode()
            response = account.delete_account(account_id)
            conn.send(response.encode())

    return None

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
            if current_client["type"] == "client":
                client_options(conn, current_client, data)
            else:
                admin_options(conn, data)
        else:
            login_id = data.split(";")[0]
            login_pwd = data.split(";")[1]
            current_client = account.login(login_id, login_pwd)
            if (current_client['success']):
                logged_in = True
            
            json_current_client = json.dumps(current_client)
            conn.send(json_current_client.encode())

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