import os
from dotenv import load_dotenv
from datetime import datetime

BASEDIR = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(BASEDIR, 'conf/.env'))


BOT_TOKEN = os.getenv('BOTTOKEN')
BOT_ID = "@ztu_liceum_status_bot"

start_date_status = datetime(2023, 9, 4)

