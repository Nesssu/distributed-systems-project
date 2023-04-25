import xml.etree.ElementTree as ET

def pay(amount, destination, account, client):
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for bank_account in account_root:
        if bank_account.find("serial_nr").text == account:
            if bank_account.find("client").text == client:
                balance = float(bank_account.find("balance").text)
                if balance >= amount:
                    for destination_account in account_root:
                        if destination_account.find("serial_nr").text == destination and destination_account.find("type").text == "payment":
                            destination_balance = float(destination_account.find("balance").text)
                            destination_balance += amount
                            destination_account.find("balance").text = str(destination_balance)
                            balance -= amount
                            bank_account.find("balance").text = str(balance)
                            account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                            return f"\nPayment made to account '{destination}'."
                else:
                    return "\nInsufficient balance!"

    return "\nCoulnd't make the payment to that account!"
