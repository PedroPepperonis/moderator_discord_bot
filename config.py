import os
import sys


BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = '!'
APPLICATION_ID = os.getenv('APPLICATION_ID')
OWNERS = os.getenv('OWNERS')
DATABASE_URL = os.getenv('DATABASE_URL')

STATUSES = ['Шо ты смотришь?', 'Слава Украине', '!help', 'Хотел бы передать привет твоей маме',
            'Криэйтед бай Педро Пепперонис', 'Ксюша, верни 700 грн', '']

if not BOT_TOKEN:
    print('Вы забыли указать токен бота')
    sys.exit()
