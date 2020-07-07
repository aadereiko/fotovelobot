class UsersModel:
    def __init__(self):
        pass

    def show_all_users(self, db, bot, message):
        users = db.get_all_users()
        cid = message.chat.id
        res = ''
        for i in range(0, len(users)):
            res += f'{i + 1}. {users[i][1]} {users[i][2]} {users[i][3]}.\n'
        bot.send_message(cid, res)