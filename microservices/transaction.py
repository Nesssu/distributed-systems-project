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
def withdraw(amount, account):
    
    return None
