import psycopg2


class Database:
    def __init__(self, db):
        self.connection = psycopg2.connect(db, sslmode='require')
        self.cursor = self.connection.cursor()

    def add_ban_word(self, server_name, server_id, channel_name, channel_id, word, reason):
        with self.connection:
            return self.cursor.execute('INSERT INTO '
                                       'banword(server_name, server_id, channel_name, channel_id, word, reason) '
                                       'VALUES(%s,%s,%s,%s,%s,%s)',
                                       (server_name, server_id, channel_name, channel_id, word, reason))

    def get_ban_word(self, channel_id):
        with self.connection:
            self.cursor.execute('SELECT word FROM banword WHERE channel_id=%s', (channel_id, ))
            return self.cursor.fetchall()

    def delete_ban_word(self, channel_id, word):
        with self.connection:
            return self.cursor.execute('DELETE FROM banword WHERE channel_id=%s AND word=%s', (channel_id, word))

    def banword_exists(self, channel_id, word):
        with self.connection:
            self.cursor.execute('SELECT word FROM banword WHERE channel_id=%s AND word=%s', (channel_id, word))
            result = self.cursor.fetchone()
            return bool(result)

    def close(self):
        self.connection.close()
