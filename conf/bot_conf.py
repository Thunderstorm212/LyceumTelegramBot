import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(BASEDIR, '.env'))

BOT_TOKEN = os.getenv('BOTTOKEN')
print(BOT_TOKEN)



