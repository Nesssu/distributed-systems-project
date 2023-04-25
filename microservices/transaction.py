import xml.etree.ElementTree as ET

def deposit(amount, destination, current_client):
    # First we check that the account is one of the users accounts. Users cannot deposit money to other users accounts.
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for bank_account in account_root:
        # First, find the bank account where the money is deposited.
        if bank_account.find("serial_nr").text == destination:
            # Then, make sure that the account belongs to the current client.
            if bank_account.find("client").text == current_client:
                # Now we can deposit the money to the account
                balance = float(bank_account.find("balance").text)
                balance += amount
                bank_account.find("balance").text = str(balance)
                # Save the changes made to the database.
                account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                return (f"\n{amount} € deposited to account {destination}.")

    return ("\nCouldn't deposit money to that account!")

def withdraw(amount, account, current_client):
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for bank_account in account_root:
        # First, find the bank account.
        if bank_account.find("serial_nr").text == account:
            # Then, check that the bank account belongs to the current client.
            if bank_account.find("client").text == current_client:
                # Then we make sure that the balance is big enough.
                balance = float(bank_account.find("balance").text)
                if balance >= amount:
                    # The withdrawal can be done.
                    balance -= amount
                    bank_account.find("balance").text = str(balance)
                    # Save the changes made to the database.
                    account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                    return (f"\n{amount} € withdrawn from the account {account}.")
                else:
                    return "\nInsufficient balance!"

    return "\nCouldn't withdraw from that account!"

def transfer(amount, destination, account, client):
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for bank_account in account_root:
        # First, find the bank account where the money is taken.
        if bank_account.find("serial_nr").text == account:
            # Then, check that it belongs to the current client.
            if bank_account.find("client").text == client:
                balance = float(bank_account.find("balance").text)
                # Check that the balance of the bank account is big enough.
                if balance >= amount:
                    for destination_account in account_root:
                        # Find the bank account where the money is supposed to be sent.
                        if destination_account.find("serial_nr").text == destination:
                            # Add the amount to the balance of the destination account
                            destination_balance = float(destination_account.find("balance").text)
                            destination_balance += amount
                            destination_account.find("balance").text = str(destination_balance)
                            # Remove the amount from the clients account
                            balance -= amount
                            bank_account.find("balance").text = str(balance)
                            # Save the chnages made to the database.
                            account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                            return f"\n{amount} € transferred from your account '{account}' to the account '{destination}'."
                else:
                    return "\nInsufficient balance!"
                        
    return "\nCouldn't transfer the money!"
