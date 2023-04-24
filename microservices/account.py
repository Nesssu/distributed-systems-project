import xml.etree.ElementTree as ET
client_tree = ET.parse("client_db.xml")
client_root = client_tree.getroot()
account_tree = ET.parse("account_db.xml")
account_root = account_tree.getroot()

# Logs the client into the server. Returns a dictionary back to the server that has
# the name, id and the type of the client.
def login(id, pwd):
    result = {}
    for client in client_root:
        login_id = client.find('login_id').text
        if login_id == id:
            password = client.find('password').text
            if password == pwd:
                result['success'] = True
                client_type = client.find('type').text
                result['type'] = client_type
                result['id'] = client.find('login_id').text
                result['name'] = client.find('name').text
                return result
            
    result['success'] = False
    return result

# Shows a quick info about the client. Name, all accounts and the type of the account.
def get_account_info(id):
    result = []
    for account in account_root:
        if account.find("client").text == id:
            result.append(account.find("serial_nr").text)
        
    return result

# Shows the balance and type of all the bank accounts the client has.
def get_balance(id):
    result = []
    for account in account_root:
        client = account.find('client').text
        if (client == id):
            dic = {
                'serial_nr': account.find('serial_nr').text,
                'balance': account.find('balance').text,
                'type': account.find('type').text
            }
            result.append(dic)
    return result

# Allows the admins to create new bank accounts for the clients.
def create_account():

    return None

# Allows the admins to delete existing accounts for the clients.
def delete_account():

    return None

# Allows admins to add new clients to the bank.
def create_client():
    
    return None

# Allows the admins to delete clients from the bank.
def delete_client():
    
    return None
