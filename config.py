import os
import sys


BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = '!'
APPLICATION_ID = os.getenv('APPLICATION_ID')
OWNERS = os.getenv('OWNERS')
DATABASE_URL = os.getenv('DATABASE_URL')

if not BOT_TOKEN:
    print('Вы забыли указать токен бота')
    sys.exit()
