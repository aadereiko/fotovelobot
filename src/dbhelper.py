import sqlite3
import xlsxwriter
import io

class DBHelper:
    def __init__(self, dbname="fotovelo.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        try:
            self.create_nomination_table()
            self.conn.commit()

            self.create_user_table()
            self.conn.commit()
        except:
            print(self.get_all_users(), 'USERS')
            print('ALREADY INITIALIZED')

    def create_user_table(self):
        self.conn.execute("""
            CREATE TABLE users (
            user_id text PRIMARY KEY,
            first_name text,
            last_name text,
            username text UNIQUE,
            email text UNIQUE,
            has_participated integer,
            is_phone integer,
            occupation text,
            has_17 integer,
            phone text UNIQUE,
            how_met text
            )
             """)

    def create_nomination_table(self):
        self.conn.execute("""
            CREATE TABLE nomination (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        """)

    def add_user(self, user):
        try:
            stmt = "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            args = (user['id'], user['first_name'], user['last_name'], user['username'], user['email'], user['has_participated'],
                    user['is_phone'], user['occupation'], user['has_17'], user['phone'], user['how_met'])
            self.conn.execute(stmt, args)
            self.conn.commit()
            print('Успешно записан', args)
        except:
            print('Errors while writing user ', user.username)

    def get_all_users(self):
        try:
            stmt = "SELECT * FROM users"
            return [x for x in self.conn.execute(stmt)]
        except:
            print('Ошибки во время запроса на всех пользователей ')

    def delete_user_table(self):
        stmt = "DELETE TABLE users"
        self.conn.execute(stmt)
        self.conn.commit()

    def write_users_to_excel(self):
        users = self.get_all_users()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("My sheet")

        headers = ('Телеграм ID', 'Имя', 'Фамилия', 'Username', 'Email', 'Участвовал ли?', 'С телефоном?', 'Занятость',
                   'Старше 17?', 'Телефон', 'Как узнал о проекте?')
        for i in range(0, len(headers)):
            worksheet.write(0, i, headers[i])

        row = 1
        for user in users:
            for i in range(0, len(user)):
                worksheet.write(row, i, user[i])
            row += 1
        workbook.close()
        return output

    # nomination api
    def add_nomination(self, name):
        try:
            stmt = "INSERT INTO nomination (name) VALUES (?)"
            args = (name,)
            self.conn.execute(stmt, args)
            self.conn.commit()
            print('Успешно записана', args)
        except:
            print('Errors while writing nomination ', name)

    def get_all_nominations(self):
        try:
            stmt = "SELECT * FROM nomination"
            return [x for x in self.conn.execute(stmt)]
        except:
            print('Ошибки во время запроса на всех пользователей ')


    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.conn.execute(stmt)]
