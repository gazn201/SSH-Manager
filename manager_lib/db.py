import sqlite3
import os
import sys
from lib.installer import manager_init

DB_PATH = os.path.expanduser("~/.ssh-manager/ssh-conf.db")

print (DB_PATH)

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
elif not os.path.exists(DB_PATH):
    print("Manager database not found!")
    PROMPT = input("Init manager?[y/n]")
    if PROMPT in ['y','Y','Yes','yes']:
        manager_init()
    else:
        print("aborting...")
        sys.exit(0)


def update_field_hosts(field, value, id):
    cursor.execute(f"UPDATE Hosts SET {field} = ? WHERE ID = ?", (value, id))
def update_field_additional(id, additional):
    cursor.execute(f"UPDATE ADDITIONALPARAMS SET PARAMETR = ?, VALUE = ? WHERE ID = ?", (additional[0], additional[1], id))
def insert_additioanl(id, additional):
    print(f"{additional}")
    cursor.execute("INSERT INTO ADDITIONALPARAMS (ID, PARAMETR, VALUE) VALUES (?, ?, ?)", (id, additional[1], additional[2]))
