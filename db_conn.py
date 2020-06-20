import sqlite3
import random
'''
conn = sqlite3.connect('gaming.db')
c = conn.cursor()
#c.execute("""DROP TABLE users """)
#c.execute("""DROP TABLE achivements """)


c.execute("""CREATE TABLE users (
            id int PRIMARY KEY,
            name text

)""")

c.execute("""CREATE TABLE achivements (
            id int PRIMARY KEY,
            name text,
            user_id int,
            time int,
            exp int,
            completed text,
            FOREIGN KEY(user_id) REFERENCES users(id)
            
)""")


conn.commit()
conn.close()
'''


class UsersDb():
    def __init__(self, id, name):
        self.id = int(id)
        self.name = name

    def show_achivements(self):
        conn = sqlite3.connect('gaming.db')
        c = conn.cursor()
        query = '''SELECT name FROM achivements where id = ?'''
        c.execute(query, self.id)

    def check_user(self):
        conn = sqlite3.connect('gaming.db')
        c = conn.cursor()
        query = '''SELECT id FROM users
        '''
        db_id = c.execute(query)
        conn.commit()
        conn.close()
        if db_id == self.id:
            return False
        else:
            return True

    def new_user(self):
        conn = sqlite3.connect('gaming.db')
        c = conn.cursor()
        id_query = """SELECT id FROM achivements"""
        achivements = c.execute(id_query)
        random_id = random.randint(1000, 10000)
        if not random_id in achivements:
            c.execute(f"""INSERT INTO users VALUES (?, ?)""",
                      (self.id, self.name)
                      )
            c.execute(
                f"""INSERT INTO achivements VALUES (?, ?, ? ,?, ?, ?)""",
                (random_id, 'time in game', self.id, 10, 100, 'False')
            )
        else:
            while random_id in achivements:
                try:
                    c.execute(f"""INSERT INTO users VALUES (?, ?)""",
                              (self.id, self.name)
                              )
                    c.execute(
                        f"""INSERT INTO achivements VALUES (?, ?, ? ,?, ?, ?)""", (random_id, 'time in game', self.id, 10, 100, 'False'))
                except sqlite3.IntegrityError:
                    random_id = random.randint(1000, 10000)

        conn.commit()
        conn.close()
