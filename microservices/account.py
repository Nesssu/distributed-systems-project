import xml.etree.ElementTree as ET
client_tree = ET.parse("client_db.xml")
client_root = client_tree.getroot()
account_tree = ET.parse("account_db.xml")
account_root = account_tree.getroot()

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
                return result
            
    result['success'] = False
    return result

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

def create_account():

    return None

def delete_account():

    return None
