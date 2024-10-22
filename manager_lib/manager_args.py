import os
from dotenv import load_dotenv

DOTENV_PATH = os.path.expanduser("~/.ssh-manager/.env")

if os.path.exists()
    load_dotenv(dotenv_path=DOTENV_PATH)
    
    SCRIPT_HOME = os.getenv('SCRIPT_HOME')
    SSH_CONFIG = os.getenv('SSH_CONFIG')
    DATABASE_PATH = os.getenv('DATABASE_PATH')

else:
    SCRIPT_HOME = os.path.expanduser("~/.ssh-manager")
    SSH_CONFIG = os.path.expanduser("~/.ssh/config")
    DATABASE_PATH = os.path.expanduser("/.ssh-manager/ssh-conf.db")

   
