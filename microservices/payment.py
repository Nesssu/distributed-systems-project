import xml.etree.ElementTree as ET

def pay(amount, destination, origin, current_client):
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    for bank_account in account_root:
        # First, find the bank account where the money is taken.
        if bank_account.find("serial_nr").text == origin:
            # Then, check that the account belongs to the current client.
            if bank_account.find("client").text == current_client:
                balance = float(bank_account.find("balance").text)
                # Then, check that the balance of the bank account is enough for the payment.
                if balance >= amount:
                    for destination_account in account_root:
                        # Find the account where the  money is sent and make sure that the account is a payment account.
                        if destination_account.find("serial_nr").text == destination and destination_account.find("type").text == "payment":
                            # Correct the balances of those accounts.
                            destination_balance = float(destination_account.find("balance").text)
                            destination_balance += amount
                            destination_account.find("balance").text = str(destination_balance)
                            balance -= amount
                            bank_account.find("balance").text = str(balance)
                            # Save the changes made to the database.
                            account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
                            return f"\nPayment made to account '{destination}'."
                else:
                    return "\nInsufficient balance!"

    return "\nCoulnd't make the payment to that account!"
