from manager_lib.db import *
from manager_lib.core import *
import yaml

def export_all_to_yaml():
    cursor.execute("SELECT HOSTNAME, ADDRESS, USERNAME, KEY, PORT FROM Hosts")
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        hostname, address, username, keyid, port = row
        key = get_keypath_by_id(keyid)
        data[hostname] = {
            'address': address,
            'key': key,
            'port': port,
            'username': username
        }
    with open('ssh-config.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

