import xml.etree.ElementTree as ET
from random import randint

# Logs the client into the server. Returns a dictionary back to the server that has
# the name, id and the type of the client.
def login(id, pwd):
    client_tree = ET.parse("client_db.xml")
    client_root = client_tree.getroot()
    current_client = {}
    for client in client_root:
        login_id = client.find('login_id').text
        if login_id == id:
            password = client.find('password').text
            if password == pwd:
                # When the ID and password are correct, the user data is added to the dictionary.
                current_client['success'] = True
                client_type = client.find('type').text
                current_client['type'] = client_type
                current_client['id'] = client.find('login_id').text
                current_client['name'] = client.find('name').text
                return current_client
    
    # If the ID or the password is incorrect, the dictionary has only one value
    # which tells the server that the login has failed
    current_client['success'] = False
    return current_client

# Returns the all the customers the bank has to the server
def get_all_clients():
    client_tree = ET.parse("client_db.xml")
    client_root = client_tree.getroot()
    clients = []
    for client in client_root:
        # Doesn't add admins to the list
        if client.find("type").text != "admin":
            # Creates a dictionary that has the ID and the name of the client
            dic = {
                "name": client.find("name").text,
                "id": client.find("login_id").text
            }
            # Adds them all to a list
            clients.append(dic)
    
    return clients

# Get all the accounts that a certain client has in the bank
def get_account_info(id):
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    accounts = []
    for account in account_root:
        if account.find("client").text == id:
            accounts.append(f'({account.find("type").text}) SERIAL NUMBER: {account.find("serial_nr").text}')
        
    return accounts

# Shows the balance and type of all the bank accounts the client has.
def get_balance(id):
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    accounts = []
    for account in account_root:
        client = account.find('client').text
        if (client == id):
            # Creating a dictionary that has all the info needed
            dic = {
                'serial_nr': account.find('serial_nr').text,
                'balance': account.find('balance').text,
                'type': account.find('type').text
            }
            # Then adding the dictionary to the end of the list
            accounts.append(dic)
        
    return accounts

# Allows the admins to create new bank accounts for the clients.
def create_account():

    return None

# Allows the admins to delete existing accounts for the clients.
def delete_account():

    return None

# Allows admins to add new clients to the bank.
def create_client(name, password):
    client_tree = ET.parse("client_db.xml")
    client_root = client_tree.getroot()
    
    client_id = randint(10000000, 99999999)
    client_element = ET.Element('client')
    name_element = ET.SubElement(client_element, 'name')
    name_element.text = name
    type_element = ET.SubElement(client_element, 'type')
    type_element.text = "client"
    id_element = ET.SubElement(client_element, 'login_id')
    id_element.text = str(client_id)
    password_element = ET.SubElement(client_element, 'password')
    password_element.text = password
    client_root.append(client_element)
    client_tree.write("client_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')

    return f"New client added with the ID {client_id}."

# Allows the admins to delete clients from the bank.
def delete_client(client_id):
    client_tree = ET.parse("client_db.xml")
    client_root = client_tree.getroot()
    account_tree = ET.parse("account_db.xml")
    account_root = account_tree.getroot()
    
    # Because we are deleting the whole client from the bank, we first delete all the accounts the client has.
    for account in account_root:
        if account.find("client").text == client_id:
            # Delete the account
            account_root.remove(account)
    
    # Then we delete the client itself.
    for client in client_root:
        if client.find("login_id").text == client_id:
            # Delete the client
            client_root.remove(client)
    
    # Save the changes to the databases
    account_tree.write("account_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
    client_tree.write("client_db.xml", xml_declaration=True, method='xml', encoding='UTF-8')
    return None
