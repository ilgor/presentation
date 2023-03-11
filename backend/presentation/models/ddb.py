import os
import sqlite3 as sql
from presentation import app


class Ddb:
    def __init__(self, lab_table: str = None):
        self.logger = app.logger
        self.database = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../database.db')

    def get_user(self, user_id):
        try:
            con = sql.connect(self.database)
            cur = con.cursor()
            cur.execute("SELECT user_id, password, group_id, room_id FROM users WHERE user_id=?", (user_id,))
            users = cur.fetchall()
            con.close()
            return users[0]
        except Exception as e:
            app.logger.warning(f'User not found?: {user_id}')
    
    def get_user_password(self, user_id):
        try:
            con = sql.connect(self.database)
            cur = con.cursor()
            cur.execute("SELECT password FROM users WHERE user_id=?", (user_id,))
            res = cur.fetchone()
            con.close()
            return res[0]
        except Exception as e:
            app.logger.warning(f'User not found?: {user_id}')
