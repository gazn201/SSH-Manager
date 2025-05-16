import sys
import ipaddress
import readline
import os
from manager_lib.db import *
from manager_lib.manager_args import SSH_CONFIG, SCRIPT_HOME
from manager_lib.installer import create_home
from colorama import Fore, Style, init

def complete_path(text, state):
    line = readline.get_line_buffer()
    path = os.path.expanduser(text)
    if os.path.isdir(path):
        files = os.listdir(path)
        matches = [os.path.join(path, f) + '/' if os.path.isdir(os.path.join(path, f)) else os.path.join(path, f) for f in files]
    else:
        dirname, basename = os.path.split(path)
        if not dirname:
            dirname = "."
        try:
            files = os.listdir(dirname)
        except FileNotFoundError:
            files = []
        matches = [os.path.join(dirname, f) for f in files if f.startswith(basename)]
    return matches[state] if state < len(matches) else None


def input_with_completion(prompt):
    readline.set_completer(complete_path)
    readline.set_completer_delims('')
    readline.parse_and_bind("bind ^I rl_complete")
    return input(prompt)

def check_input(prompt):
    user_input = input(prompt).strip()
    if user_input:
        return user_input
    else:
        print(Fore.RED + f"String is empty!" + Style.RESET_ALL)
        return None

#Hostaname
def get_hostname():
    while True:
        hostname = check_input(Fore.GREEN + f"Enter hostname: " + Style.RESET_ALL)
        if hostname:
            query_hostname = "SELECT HOSTNAME FROM Hosts WHERE HOSTNAME = ?"
            cursor.execute(query_hostname, (hostname,))
            result = cursor.fetchone()
            if result:
                print(Fore.RED + f"Hostname {result[0]} already exist!" + Style.RESET_ALL)
            else:
                return hostname
        else:
            pass

#IP Address
def valid_address():
    while True:
        address = input(Fore.GREEN + f"Enter IP address: " + Style.RESET_ALL)
        try:
            ip = ipaddress.ip_address(address)
            return address
        except ValueError:
            print(Fore.RED + f"IP address not valid!" + Style.RESET_ALL)

def get_address():
    while True:
        print(Fore.GREEN + f"IP address or Domain? (Default IP address)\n[1] IP Address\n[2] Domain" + Style.RESET_ALL)
        x = input(Fore.GREEN + f"Choose an option: " + Style.RESET_ALL)
        if x == '1' or x == '':
            address = valid_address()
            return address
        elif x == '2':
            domain = check_input(Fore.GREEN + f"Enter domain: " + Style.RESET_ALL)
            if domain:
                address = domain
                return address
            else:
                pass
        else:
            print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)



#USERNAME
def get_username():
    while True:
        username = check_input(Fore.GREEN + f"Enter username: " + Style.RESET_ALL)
        if username:
            return username
        else:
            pass

#PORT
def get_port():
    while True:
        choice = input(Fore.GREEN + f"Using default port? [Y/n]: " + Style.RESET_ALL)
        if choice.lower() == 'y' or choice == '':
            port = '22'
            return port
        elif choice.lower() == 'n':
            while True:
                port = check_input(Fore.GREEN + f"Enter port: " + Style.RESET_ALL)
                if port:
                    return port
                else:
                    pass
        else:
            print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)

#KEY
def list_keys():
    cursor.execute("SELECT KEYID, KEYNAME FROM KEYS")
    rows = cursor.fetchall()
    for row in rows:
        print(f"[{row[0]}] {row[1]}")

def get_keypath_by_id(record_id):
    cursor.execute("SELECT KEYPATH FROM KEYS WHERE KEYID = ?", (record_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(Fore.RED + f"{record_id} not found." + Style.RESET_ALL)
        return None

def key_definition():
    while True:
        key_choice = input(Fore.GREEN + f"Key ID (l for list, a for add new key): " + Style.RESET_ALL)
        if key_choice.isdigit():
            record_id = int(key_choice)
            path = get_keypath_by_id(record_id)
            if path:
                key = record_id
                return key
            break
        elif key_choice == 'l':
            list_keys()
        elif key_choice == 'a':
            addNewKey()
        else:
            print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)

def define_additional():
    while True:
        i = input(Fore.GREEN + f"Do you want to add additional parameters? [y/N]: " + Style.RESET_ALL)
        if i.lower() == 'y':
            additional = True
            while True:
                parametr = check_input(Fore.GREEN + f"Enter additional parametr: " + Style.RESET_ALL)
                if parametr:
                    break
                else:
                    pass
            value = input(Fore.GREEN + f"Enter value: " + Style.RESET_ALL)
            return additional, parametr, value
        elif i.lower() == 'n' or i == '':
            additional = False
            return [additional]
        else:
            print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)

def edit_additional(id):
    while True:
        parametr = check_input(Fore.GREEN + f"Enter additional parametr: " + Style.RESET_ALL)
        if parametr:
            break
        else:
            pass
    value = input(Fore.GREEN + f"Enter value: " + Style.RESET_ALL)
    cursor.execute("SELECT PARAMETR FROM ADDITIONALPARAMS WHERE ID = ?", (id,))
    additional_parametr = cursor.fetchone()
    if additional_parametr:
        additional = [parametr, value]
        update_field_additional(id, additional)
    else:
        additional = [True, parametr, value]
        insert_additioanl(id, additional)

def createBaseConfig(*args, **kwargs):
    hostname = get_hostname()
    address = get_address()
    username = get_username()
    port = get_port()
    key = key_definition()
    additional = define_additional()
    print(f"\n")
    print(f"Hostname = {hostname}")
    print(f"Address = {address}")
    print(f"Username = {username}")
    print(f"Port = {port}")
    print(f"Key = {key}")
    if additional[0]:
        print(f"Parametr = {additional[1]}")
        print(f"Value = {additional[2]}")
    else:
        pass
    choice = input(Fore.GREEN + f"\nIs config correct? [Y/n]" + Style.RESET_ALL)
    if choice.lower() == 'y' or choice == '':
        cursor.execute("SELECT MAX(ID) FROM Hosts")
        last_id = cursor.fetchone()[0]
        new_id = (last_id + 1) if last_id else 1
        cursor.execute("INSERT INTO Hosts (ID, HOSTNAME, ADDRESS, USERNAME, KEY, PORT) VALUES (?, ?, ?, ?, ?, ?)", (new_id, hostname, address, username, key, port))
        if additional[0]:
            insert_additioanl(new_id, additional)
        else:
            pass
        conn.commit()
    elif choice.lower() == 'n':
        sys.exit(0)
    else:
        print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)


def generateSSHConfig():
    cursor.execute("SELECT ID, HOSTNAME, ADDRESS, USERNAME, KEY, PORT FROM Hosts")
    rows = cursor.fetchall()
    with open(SSH_CONFIG, 'w') as file:
        for row in rows:
            id, hostname, address, user, key, port = row
            cursor.execute("SELECT KEYPATH FROM KEYS WHERE KEYID = ?", (key,))
            keypath = cursor.fetchone()
            file.write(f"Host {hostname}\n")
            file.write(f"\tHostName {address}\n")
            file.write(f"\tUser {user}\n")
            file.write(f"\tPort {port}\n")
            file.write(f"\tIdentityFile {keypath[0]}\n")
            cursor.execute("SELECT PARAMETR, VALUE FROM ADDITIONALPARAMS WHERE ID = ?", (id,))
            additional_params = cursor.fetchall()
            for param, value in additional_params:
                file.write(f"\t{param} {value}\n")
            file.write(f"\n")


def addNewKey():
    keypath = input_with_completion(Fore.GREEN + f"Enter path: " + Style.RESET_ALL)
    keyname = input(Fore.GREEN + f"Enter visible name for key: " + Style.RESET_ALL)
    cursor.execute("SELECT MAX(KEYID) FROM KEYS")
    last_id = cursor.fetchone()[0]
    new_id = (last_id + 1) if last_id else 1
    cursor.execute("INSERT INTO KEYS (KEYID, KEYNAME, KEYPATH) VALUES (?, ?, ?)", (new_id, keyname, keypath))
    conn.commit()
    print(Fore.GREEN + f"Key have been added: [{new_id}] {keyname}" + Style.RESET_ALL)

def deleteKey(arg):
    key_id = arg
    cursor.execute("SELECT KEYNAME, KEYPATH FROM KEYS WHERE KEYID = ?", (key_id,))
    key_info = cursor.fetchone()
    key_name, key_path = key_info
    cursor.execute("SELECT ID, HOSTNAME, ADDRESS FROM Hosts WHERE KEY = ?", (key_id,))
    host_list = cursor.fetchall()
    if host_list:
        print(Fore.RED + f"Key [{key_id}] {key_name} is using in hosts:\n" + Style.RESET_ALL)
        for row in host_list:
            id, hostname, address = row
            print(Fore.GREEN + f"ID {id} ;; Hostname {hostname} ;; Address {address}" + Style.RESET_ALL)
        sys.exit(1)
    else:
        print(Fore.GREEN + f"Key [{key_id}] {key_name} don't use any hosts." + Style.RESET_ALL)
        i = input(Fore.RED + f"Do you want to remove the key [{key_id}] {key_name}? [yes/no]: " + Style.RESET_ALL)
        if i.lower() == 'yes':
            cursor.execute("DELETE FROM KEYS where KEYID = ?", (key_id,))
        elif i.lower() == 'no' or i.lower() == 'n':
            sys.exit(Fore.GREEN + f"Operation was canceled." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)
        conn.commit()
        print(Fore.GREEN + f"[{key_id}] {key_name} was successfully removed." + Style.RESET_ALL)

def searchHosts(arg):
    searchObject = f"%{arg}%"
    cursor.execute(f"SELECT ID, HOSTNAME, ADDRESS FROM Hosts WHERE HOSTNAME LIKE '{searchObject}' or ADDRESS LIKE '{searchObject}'")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            id, hostname, address = row
            print(Fore.GREEN + f"ID {id} ;; Hostname {hostname} ;; Address {address}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"No matches found" + Style.RESET_ALL)


def parse_values(value_str):
    values = []
    HostIDs = value_str.split(',')
    for part in HostIDs:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            start, end = int(start), int(end)
            values.extend(range(start, end + 1))
        else:
            values.append(int(part))
    return values
def deleteHosts(arg):
    value_str = arg
    hostIDs = parse_values(value_str)
    success_count = 0
    unsuccess_count = 0
    id_found = []
    id_not_found = []
    for host in hostIDs:
        cursor.execute("SELECT ID FROM Hosts WHERE ID = ?", (host,))
        id = cursor.fetchone()
        if id:
            id_found.append(host)
            success_count += 1
        else:
            id_not_found.append(host)
            unsuccess_count += 1
    for host in id_not_found:
        print(Fore.RED + f"{host} can't be removed. Not found!" + Style.RESET_ALL)
    print(f"\n")
    for host in id_found:
        cursor.execute("SELECT HOSTNAME FROM Hosts WHERE ID = ?", (host,))
        hostname = cursor.fetchone()
        print(Fore.GREEN + f"ID: {host} ;; Hostname {hostname[0]} can be deleted!" + Style.RESET_ALL)
    print(f"\n")
    while True:
        i = input(Fore.RED + f"Remove {success_count} hosts? [yes/no]: " + Style.RESET_ALL)
        if i.lower() == 'yes':
            for host in id_found:
                cursor.execute("DELETE FROM Hosts where ID = ?", (host,))
                cursor.execute("SELECT ID FROM ADDITIONALPARAMS WHERE ID = ?", (host,))
                additional_id = cursor.fetchone()
                if additional_id:
                    cursor.execute("DELETE FROM ADDITIONALPARAMS WHERE ID = ?", (host,))
                else:
                    pass
            break
        elif i.lower() == 'no' or i.lower() == 'n':
            sys.exit(Fore.GREEN + f"Operation was canceled." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)
    conn.commit()
    print(Fore.GREEN + f"{success_count} was successfully removed / {unsuccess_count} was not removed." + Style.RESET_ALL)

def is_integer(int_value):
    try:
        int(int_value)
        return True
    except ValueError:
        return False


def editHosts(arg, *args, **kwargs):
    int_value = arg
    id = arg
    if is_integer(int_value):
        cursor.execute("SELECT ID, HOSTNAME, ADDRESS, USERNAME, KEY, PORT FROM Hosts WHERE ID = ?", (id,))
        config = cursor.fetchone()
        if config:
            id, hostname, address, username, keyid, port = config
            cursor.execute("SELECT KEYNAME FROM KEYS WHERE KEYID = ?", (keyid,))
            key = cursor.fetchone()
            cursor.execute("SELECT PARAMETR, VALUE FROM ADDITIONALPARAMS WHERE ID = ?", (id,))
            additional = cursor.fetchone()
            print(Fore.GREEN + f"\nID: {id}\nHostname: {hostname}\nAddress: {address}\nUsername: {username}\nKey: {key[0]}\nPort: {port}" + Style.RESET_ALL)
            if additional:
                print(Fore.GREEN + f"Parametr = {additional[0]}" + Style.RESET_ALL)
                if additional[1]:
                    print(Fore.GREEN + f"Value = {additional[1]}\n" + Style.RESET_ALL)
            print(Fore.GREEN + f"What do you want to edit?" + Style.RESET_ALL)
            options = {
                'h': lambda: update_field_hosts('HOSTNAME', get_hostname(), id),
                'a': lambda: update_field_hosts('ADDRESS', get_address(), id),
                'u': lambda: update_field_hosts('USERNAME', get_username(), id),
                'k': lambda: update_field_hosts('KEY', key_definition(), id),
                'p': lambda: update_field_hosts('PORT', get_port(), id),
                'ad': lambda: edit_additional(id),
                'all': lambda: (deleteHosts(arg), createBaseConfig()),
                'c': lambda: sys.exit(Fore.RED + f"Operation was canceled." + Style.RESET_ALL)
            }
            while True:
                print(Fore.GREEN + f"You can select next options:" + Style.RESET_ALL)
                print(Fore.GREEN + f"hostname (h), address (a), username (u), key (k), port (p), additional (ad)" + Style.RESET_ALL)
                print(Fore.GREEN + f"all (all) or cancel (c)" + Style.RESET_ALL)
                choice = input(Fore.GREEN + f"Please enter your option: " + Style.RESET_ALL)
                if choice in options:
                    options[choice]()
                    break
                else:
                    print(Fore.RED + f"Incorrect input, try again." + Style.RESET_ALL)
            conn.commit()
        else:
            sys.exit(Fore.RED + f"Config not found!" + Style.RESET_ALL)
    else:
        sys.exit(Fore.RED + f"Config with ID {id} does not exist!" + Style.RESET_ALL)


#CHECK FOR ENV
if not os.path.exists(f"{SCRIPT_HOME}/.env"):
    create_home()
