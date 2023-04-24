import socket
from getpass import getpass
import json

HOST = "127.0.0.1"
PORT = 1234

def client_menu():
    print("\n*** MENU ***")
    print("1) Show balance")
    print("2) Deposit money")
    print("3) Withdraw money")
    print("4) Transfer money")
    print("5) Make a payment")
    print("6) About the account")
    print("0) Logout")
    choice = input("\nYour choice: ")
    return choice

def admin_menu():
    print("\n*** MENU ***")
    print("1) Get all clients")
    print("2) Add new client")
    print("3) Delete client")
    print("4) Add new bank account")
    print("5) Delete bank account")
    print("0) Logout")
    choice = input("\nYour choice: ")
    return choice

def client_front_end(client):
    print("\n*** CLIENT PAGE ***\n")
    while True:
        choice = client_menu()
        match choice:
            case "1":
                print("\n*** BALANCE ***")
                client.send('1'.encode())
                json_account_data = client.recv(1024).decode()
                account_data = json.loads(json_account_data)
                for account in account_data:
                    print("\nSERIAL NUMBER: " + account['serial_nr'])
                    print("TYPE: " + account['type'])
                    print("BALANCE: " + account['balance'] + " €")

            case "2":
                print("\n*** DEPOSIT *** \n")
                try:
                    client.send("2".encode())
                    amount = float(input("Amount: "))
                    destination = input("Account (Serial number): ")
                    info = str(amount) + ";" + destination
                    client.send(info.encode())
                    response = client.recv(1024).decode()
                    print(response)
                except Exception:
                    print("Error occured while getting the amount!")

            case "3":
                print("\n*** WITHDRAW ***\n")
                try:
                    client.send("3".encode())
                    amount = float(input("Amount: "))
                    account = input("Account (Serial number): ")
                    info = str(amount) + ";" + account
                    client.send(info.encode())
                    response = client.recv(1024).decode()
                    print(response)
                except Exception:
                    print("Error occured while getting the amount!")

            case "4":
                print("\n*** TRANSFER ***")
                try:
                    client.send("4".encode())
                    amount = float(input("Amount: "))
                    account = input("Account (Serial number): ")
                    destination = input("Destination (Serial number): ")
                    info = str(amount) + ";" + account + ";" + destination
                    client.send(info.encode())
                    response = client.recv(1024).decode()
                    print(response)
                except Exception:
                    print("Error occured while trying to transfer money!")

            case "5":
                print("\n*** PAYMENT ***")
                try:
                    client.send("5".encode())
                    amount = float(input("Amount: "))
                    account = input("Account (Serial number): ")
                    destination = input("Destination (Serial number): ")
                    info = str(amount) + ";" + account + ";" + destination
                    client.send(info.encode())
                    response = client.recv(1024).decode()
                    print(response)
                except Exception:
                    print("Error occured while making a payment!")

            case "6":
                print("\n*** ABOUT ***")
                client.send('6'.encode())
                json_client_data = client.recv(1024).decode()
                client_data = json.loads(json_client_data)
                print("NAME: " + client_data["name"])
                print("TYPE: " + client_data["type"])
                if (client_data["accounts"] == []):
                    print("ACCOUNTS: No accounts yet")
                else:
                    print("ACCOUNTS:")
                    for account in client_data["accounts"]:
                        print("SERIAL NUMBER: " + account)

            case "0":
                break

            case _:
                print("Command not recognised. Try again!")

    print("\nLogged out ...")
    return None

def admin_front_end(client):
    print("\n*** ADMIN PAGE ***\n")
    while True:
        choice = admin_menu()
        match choice:
            case "1":
                print("\n*** ALL CLIENTS ***\n")
                client.send("1".encode())
                json_clients = client.recv(1024).decode()
                clients = json.loads(json_clients)
                for item in clients:
                    print(item["name"])
                    print(item["id"] + "\n")

            case "2":
                print("\n*** ADD NEW CLIENT ***\n")
                client.send("2".encode())
                name = input("Name of the client: ")
                password = getpass("Password (4 digits): ")
                info = name + ";" + password
                client.send(info.encode())
                response = client.recv(1024).encode()
                print(response)

            case "3":
                print("\n*** DELETE CLIENT ***\n")
                client.send("3".encode())
                client_id = input("Client ID: ")
                client.send(client_id.encode())
                response = client.recv(1024).decode()
                print(response)

            case "4":
                print("\n*** ADD NEW BANK ACCOUNT ***\n")
                client.send("4".encode())
                client_id = input("Cient ID: ")
                account_type = input("Account type: (checking/payment): ")
                info = client_id + ";" + account_type
                client.send(info.encode())
                response = client.recv(1024).decode()
                print(response)

            case "5":
                print("\n*** DELETE BANK ACCOUNT ***\n")
                client.send("5".encode())
                account_id = input("Account ID: ")
                client.send(account_id.encode())
                response = client.recv(1024).decode()
                print(response)

            case "0":
                break

            case _:
                print("Command not recognised. Try again!")

    print("\nLogged out ...")
    return None

def run_client():
    client = socket.socket()
    client.connect((HOST, PORT))

    print("\n*** WELCOME TO ONLINE BANK ***")
    print("\nLogin to Continue")
    id = input("ID: ")
    password = getpass()
    login_data = id + ";" + password
    client.send(login_data.encode())
    json_user = client.recv(1024).decode()
    user = json.loads(json_user)
    print(user)
    if user["success"]:
        if user["type"] == "admin":
            admin_front_end(client)
        else:
            client_front_end(client)
    else:
        print("Invalid credentials. Quitting the program ...")

    client.close()
    return None

if __name__ == "__main__":
    run_client()
