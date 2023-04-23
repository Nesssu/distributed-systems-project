import socket
from getpass import getpass
import json

HOST = "127.0.0.1"
PORT = 55555

def menu():
    print("\n*** MENU ***")
    print("1) Show balance")
    print("2) Deposit money")
    print("3) Withdraw money")
    print("4) Transfer money")
    print("5) Make a payment")
    print("0) Log out")
    choice = input("\nYour choice: ")
    return choice

def run_client():
    client = socket.socket()
    client.connect((HOST, PORT))

    print("\n*** WELCOME TO ONLINE BANK ***")
    print("\nLogin to Continue")
    id = input("ID: ")
    password = getpass()
    login_data = id + ";" + password
    client.send(login_data.encode())
    data = client.recv(1024).decode()
    if data == "proceed":
        while True:
            choice = menu()
            match choice:
                case "1":
                    print("\n*** BALANCE ***")
                    client.send('1'.encode())
                    json_account_data = client.recv(1024).decode()
                    account_data = json.loads(json_account_data)
                    print(account_data)
                case "2":
                    print("\n*** DEPOSIT ***")
                    try:
                        amount = float(input("Amount: "))
                        # Send the amount to the transfer microservice
                        print(f"{amount} € deposited to your account.")
                    except Exception:
                        print("Error occured while getting the amount!")
                case "3":
                    print("\n*** WITHDRAW ***")
                    try:
                        amount = float(input("Amount: "))
                        # Send the amount to the transfer microservice
                        print(f"{amount} € withdrawn from your account.")
                    except Exception:
                        print("Error occured while getting the amount!")
                case "4":
                    print("\n*** TRANSFER ***")
                    try:
                        destination = input("Destination ID: ")
                        amount = float(input("Amount: "))
                        # Send the destination and amount to the transfer microservice
                        print(f"{amount} € transferred to account {destination}.")
                    except Exception:
                        print("Error occured while trying to transfer money!")
                case "5":
                    print("\n*** PAYMENT ***")
                    try:
                        destination = input("Destination Name: ")
                        amount = float(input("Amount: "))
                        # Send the destination and amount to the payment microservice
                    except Exception:
                        print("Error occured while making a payment!")
                case "0":
                    break
                case _:
                    print("Command not recognised. Try again!")

    print("\nLogged out ...")
    client.close()
    return None

if __name__ == "__main__":
    run_client()
