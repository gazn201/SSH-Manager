import sqlite3
import os
from os import environ
import sys
from pathlib import Path
from manager_lib.manager_args import DATABASE_PATH

DB_PATH = os.path.expanduser(DATABASE_PATH)
USER_HOME = Path.home()
SCRIPT_HOME = f"{USER_HOME}/.ssh-manager"


def init_db(env_path):
    conn = sqlite3.connect(f'{env_path}')
    cursor = conn.cursor()
    #Create Hosts table
    cursor.execute("CREATE TABLE 'Hosts'(ID INT PRIMARY KEY NOT NULL,HOSTNAME TEXT NOT NULL,ADDRESS CHAR(15),USERNAME TEXT NOT NULL,KEY INT NOT NULL,PORT INTEGER)")
    #Create Keys table
    cursor.execute("CREATE TABLE 'KEYS'(KEYID INT PRIMARY KEY NOT NULL,KEYNAME TEXT NOT NULL,KEYPATH TEXT NOT NULL)")
    #Create Additional Parametres table
    cursor.execute("CREATE TABLE 'ADDITIONALPARAMS'(KEYID INT NOT NULL,PARAMETR TEXT NOT NULL,VALUE TEXT)")

def create_home():
    if not os.path.exists(SCRIPT_HOME):
        #Create script home
        print(f"Creating script directory in {SCRIPT_HOME}")
        Path(SCRIPT_HOME).mkdir(parents=True, exist_ok=True)
        with open(f"{SCRIPT_HOME}/.env", "w") as env:
            env.write(f"SCRIPT_HOME='{SCRIPT_HOME}' \nSSH_CONFIG='{USER_HOME}/.ssh/config' \nDATABASE_PATH='{SCRIPT_HOME}/ssh-conf.db'")
    elif not os.path.exists(f"{SCRIPT_HOME}/.env"):
        print(".env not found, creating it")
        with open(f"{SCRIPT_HOME}/.env", "w") as env:
            env.write(f"SCRIPT_HOME='{SCRIPT_HOME}' \nSSH_CONFIG='{USER_HOME}/.ssh/config' \nDATABASE_PATH='{SCRIPT_HOME}/ssh-conf.db'")
    elif os.path.exists(f"{SCRIPT_HOME}/.env"):
        print("Find existing .env, script will use it!")
        pass

#def add_path(shell):
#    supported_shells = ['','','']
#    if shell in  supported_shells:
#        with open(f"{USER_HOME}/.zshrc", "r+") as shell:
#            for line in shell:
#                if f"export PATH=$PATH:{SCRIPT_HOME}" in line:
#                    print("Path already added! well done!")
#                    sys.exit(0)
#            else:
#                print("Adding path for zsh")
#                shell.write(f"export PATH=$PATH:{SCRIPT_HOME}")

def manager_init():
    SSH_OLD = f"{USER_HOME}/.ssh/config"
    if os.path.exists(f"{SSH_OLD}"):
        PROMPT = input(f"found config in {SSH_OLD}, is it actual config?[y/n]: ")
        if PROMPT in ['y', 'Y','yes','Yes']:
            print("Working with this...")
        elif PROMPT in ['n','N','no','No']:
            SSH_OLD = input("Absolute path to yours ssh config directory[If not exist will be created]: ")
    
    if os.path.exists(f"{SSH_OLD}") and not os.path.exists(SCRIPT_HOME):
        while True:
            BACK_BOOL = input("Backup your existing .ssh directory?[y/n]: ")
            if BACK_BOOL in ['y','Y','Yes','yes']:
                print(f"Backupin' {SSH_OLD} to {USER_HOME}/.ssh-before-manager")
                Path(f"{USER_HOME}/.ssh_before_manager").mkdir(parents=True, exist_ok=True)
                os.system(f"cp -r {SSH_OLD} {USER_HOME}/.ssh_before_manager")
                break
            elif BACK_BOOL in ['n','N','no','No']:
                print("Skippin' backup")
                break
            else:
                print("Unexpected answer!")
    elif not os.path.exists(f"{USER_HOME}/.ssh"):
        print(".ssh not found ->")
        print("Creating .ssh directory ->")
        Path(f"{USER_HOME}/.ssh").mkdir(mode=0o700, exist_ok=True)
        print("Creating config")
        if not os.path.exists(f"{USER_HOME}/.ssh/config"):
            with open(f'{USER_HOME}/.ssh/config', 'w') as fp:
                pass
   
#TODO IF STANDART DATABASE NOT EXISTING, CHECK .ENV, IF THERE IS NO .ENV AND DATABASE IN DEFAULT WAY, CREATE NEW

    #if os.path.exists(SCRIPT_HOME) and os.path.exists(f"{SCRIPT_HOME}/ssh-conf.db"):
    if os.path.exists(SCRIPT_HOME):
        print("ssh-manager directory already exists!")
    
        if os.path.exists(DB_PATH):
            print("ssh-conf database exists! Skipping the creation...")
            pass
        elif not os.path.exists(DB_PATH):
            init_db(DB_PATH)
        if not os.path.exists(f"{SCRIPT_HOME}/.env"):
            create_home()

    elif not os.path.exists(SCRIPT_HOME):
        create_home()
        init_db(DB_PATH)
#TODO

#    USER_SHELL = environ['SHELL']
#    
#    if USER_SHELL == '/bin/bash':
#        with open(f"{USER_HOME}/.bashrc", "r+") as shell:
#            for line in shell:
#                if f"export PATH=$PATH:{SCRIPT_HOME}" in line:
#                    print("Path already added! well done!")
#                    sys.exit(0)
#            else:
#                print("Adding path for bash")
#                shell.write(f"export PATH=$PATH:{SCRIPT_HOME}")
#    elif USER_SHELL == '/bin/zsh':
#        with open(f"{USER_HOME}/.zshrc", "r+") as shell:
#            for line in shell:
#                if f"export PATH=$PATH:{SCRIPT_HOME}" in line:
#                    print("Path already added! well done!")
#                    sys.exit(0)
#            else:
#                print("Adding path for zsh")
#                shell.write(f"export PATH=$PATH:{SCRIPT_HOME}")
#    else:
#        print(f"Sorry! Uknown shell, add this to yours .[$SHELL]rc file: \n export PATH=$PATH:{SCRIPT_HOME}")

