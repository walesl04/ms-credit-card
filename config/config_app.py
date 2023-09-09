from dotenv import load_dotenv
import os
from pathlib import Path

base_dir = Path(__file__)
path_env = base_dir.joinpath('../../', '.env').resolve()

load_dotenv(path_env)

class Config:
    DEBUG = os.environ.get('DEBUG', 'True')
    ENV = os.environ.get('ENVIROMENT', 'development')
    SECRET_KEY = os.environ.get('SECRET_KEY', '#9S@Q&8@#*W')


print(Config.ENV)