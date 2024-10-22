import sqlite3
import os
import sys

DB_PATH = os.path.expanduser("~/.ssh-manager/ssh-conf.db")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
else:
    print("Manager database not found! Did you run 'ssh-manager init' ?")
    sys.exit(1)

def update_field_hosts(field, value, id):
    cursor.execute(f"UPDATE Hosts SET {field} = ? WHERE ID = ?", (value, id))
def update_field_additional(id, additional):
    cursor.execute(f"UPDATE ADDITIONALPARAMS SET PARAMETR = ?, VALUE = ? WHERE ID = ?", (additional[0], additional[1], id))
def insert_additioanl(id, additional):
    print(f"{additional}")
    cursor.execute("INSERT INTO ADDITIONALPARAMS (ID, PARAMETR, VALUE) VALUES (?, ?, ?)", (id, additional[1], additional[2]))
