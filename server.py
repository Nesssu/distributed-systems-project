import socket
import threading
import microservices.account as account
import microservices.transaction as transaction
import microservices.payment as payment
import json

HOST = "127.0.0.1"
PORT = 1234

def client_options(conn, current_client, data):
    # This handles the request made by the normal clients
    match data:
        case "1":
            # The bank account data is fetch from the microservice and then sent back to the client.
            account_data = account.get_balance(current_client['id'])
            json_account_data = json.dumps(account_data)
            conn.sendall(json_account_data.encode())

        case "2":
            # First the amount and the destination account is recieved from the client
            info = conn.recv(1024).decode()
            amount = float(info.split(";")[0])
            destination = info.split(";")[1]
            # Then, the data is sent to the transaction microservice and the response is sent back to the client.
            response = transaction.deposit(amount, destination, current_client["id"])
            conn.send(response.encode())

        case "3":
            # Like with the deposit, the amount and the account are received from the client.
            info = conn.recv(1024).decode()
            amount = float(info.split(";")[0])
            bank_account = info.split(";")[1]
            # Then, the data is sent to the transaction microservice and the response is sent back to the client.
            response = transaction.withdraw(amount, bank_account, current_client["id"])
            conn.send(response.encode())

        case "4":
            # First the amount and both (origin and destination) accounts are received from the client.
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            amount = float(info_split[0])
            bank_account = info_split[1]
            destination = info_split[2]
            # Then, the data is sent to the transaction microservice and the response is sent to the client.
            response = transaction.transfer(amount, destination, bank_account, current_client["id"])
            conn.send(response.encode())

        case "5":
            # Works exactly like the transaction, but with the payment accounts.
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            amount = float(info_split[0])
            bank_account = info_split[1]
            destination = info_split[2]
            response = payment.pay(amount, destination, bank_account, current_client["id"])
            conn.send(response.encode())

        case "6":
            # First, get the account data from the account microservice.
            accounts = account.get_account_info(current_client["id"])
            result = {
                "name": current_client["name"],
                "type": current_client["type"],
                "accounts": accounts
            }
            json_result = json.dumps(result)
            # Then, send it to the client.
            conn.sendall(json_result.encode())

    return None

def admin_options(conn, data):
    # This handles the request made bu the admins.
    match data:
        case "1":
            # The data is retrived from the account microservice and then sent to the client.
            clients = account.get_all_clients()
            json_clients = json.dumps(clients)
            conn.sendall(json_clients.encode())

        case "2":
            # Receive the name and the password from the client
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            name = info_split[0]
            password = info_split[1]
            # Send the data to the account microservice.
            response = account.create_client(name, password)
            conn.send(response.encode())

        case "3":
            # Get the client ID from the client, send it to the account microservice and the send the response back to the client.
            client_id = conn.recv(1024).decode()
            response = account.delete_client(client_id)
            conn.send(response.encode())

        case "4":
            # Receive the client ID and the account type from the client.
            info = conn.recv(1024).decode()
            info_split = info.split(";")
            client_id = info_split[0]
            account_type = info_split[1]
            # Send the data to the account microservice and the response back to the client.
            response = account.create_account(client_id, account_type)
            conn.send(response.encode())

        case "5":
            # Receive the account ID from the client
            account_id = conn.recv(1024).decode()
            # Send the account ID to the account microservice and the response back to the client.
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
        # If the client is logged in, show the manus based on the clients type.
        if logged_in:
            if current_client["type"] == "client":
                client_options(conn, current_client, data)
            else:
                admin_options(conn, data)
        # If the client hasn't logged in, send the data to the server to be authenticated.
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