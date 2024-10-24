import os
from dotenv import load_dotenv

DOTENV_PATH = os.path.expanduser("~/.ssh-manager/.env")

if os.path.exists(DOTENV_PATH):
    load_dotenv(dotenv_path=DOTENV_PATH,override=True)
    
    SCRIPT_HOME = os.getenv('SCRIPT_HOME')
    SSH_CONFIG = os.getenv('SSH_CONFIG')
    DATABASE_PATH = os.getenv('DATABASE_PATH')

else:
    print(".env not found in script home, using default values")
    SCRIPT_HOME = os.path.expanduser("~/.ssh-manager")
    SSH_CONFIG = os.path.expanduser("~/.ssh/config")
    DATABASE_PATH = os.path.expanduser("~/.ssh-manager/ssh-conf.db")
