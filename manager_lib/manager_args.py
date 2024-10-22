import os
from dotenv import load_dotenv


DOTENV_PATH = os.path.expanduser("~/.ssh-manager/.env")
load_dotenv(dotenv_path=DOTENV_PATH)
