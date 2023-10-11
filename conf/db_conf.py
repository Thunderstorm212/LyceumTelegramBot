import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(f"../{__name__}"))
load_dotenv(os.path.join(BASEDIR, 'conf/.env'))


DB_TOKEN = os.getenv('DBTOKEN')
DB_USER = os.getenv('DBUSER')



