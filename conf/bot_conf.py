import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(f"../{__name__}"))
load_dotenv(os.path.join(BASEDIR, 'conf/.env'))


BOT_TOKEN = os.getenv('BOTTOKEN')
BOT_ID = "@test_develop_bot"



