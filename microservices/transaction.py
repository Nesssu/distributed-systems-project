import xml.etree.ElementTree as ET

# Deposits money from the users account
def deposit(amount, destination, client):
    # First we check that the account is one of the users accounts. Users cannot deposit money to other users accounts.
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for account in account_root:
        if (account.find("serial_nr").text == destination):
            if (account.find("client").text == client):
                # Now we can deposit the money to the account
                balance = float(account.find("balance").text)
                balance += amount
                account.find("balance").text = str(balance)
                account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                return (f"\n{amount} € deposited to account {destination}.")

    return ("\nCouldn't deposit money to that account!")

# Withdraws money from the users account. Only possible if the balance is big enough.
def withdraw(amount, account, client):
    # Like with the deposit, first we check that the account is the clients own account.
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for bank_account in account_root:
        if bank_account.find("serial_nr").text == account:
            if bank_account.find("client").text == client:
                # Then we make sure that the balance is big enough
                balance = float(bank_account.find("balance").text)
                if balance >= amount:
                    balance -= amount
                    bank_account.find("balance").text = str(balance)
                    account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                    return (f"\n{amount} € withdrawn from the account {account}.")
                else:
                    return ("Insufficient balance!")

    return ("Couldn't withdraw from that account!")

# Transfer money between accounts
def transfer(amount, destination, account, client):
    # First we check that the account is the clients' who is doing the transfer
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for bank_account in account_root:
        if bank_account.find("serial_nr").text == account:
            if bank_account.find("client").text == client:
                balance = float(bank_account.find("balance").text)
                if balance >= amount:
                    for destination_account in account_root:
                        if destination_account.find("serial_nr").text == destination:
                            # Add the amount to the balance of the destination account
                            destination_balance = float(destination_account.find("balance").text)
                            destination_balance += amount
                            destination_account.find("balance").text = str(destination_balance)
                            # Remove the amount from the clients account
                            balance -= amount
                            bank_account.find("balance").text = str(balance)
                            account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                            return f"{amount} € transferred from your account {account} to the account {destination}."
                else:
                    return "Insufficient balance!"
                        
    return "Couldn't transfer the money!"
