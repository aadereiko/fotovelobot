import telebot

from telebot import types
from src.dbhelper import DBHelper
import src.bot_config as conf
from src.sign_up import SignUpModel
from src.usersModel import UsersModel

bot = telebot.TeleBot(conf.TOKEN)
db = DBHelper()
su = SignUpModel()
um = UsersModel()
# SIGN UP
@bot.message_handler(commands=["sign_up"])
def sign_up_cmd(message):
    su.sign_up_cmd_handler(message, bot)

# inputted nothing
@bot.message_handler(func=lambda message: su.get_step_user_id(message.chat.id) == 1)
def email_handler(message):
    su.email_handler(message, bot)

# inputted email
@bot.message_handler(func=lambda message: su.get_step_user_id(message.chat.id) == 2)
def first_name_handler(message):
    su.first_name_handler(message, bot)

# inputted email, fN
@bot.message_handler(func=lambda message: su.get_step_user_id(message.chat.id) == 3)
def last_name_handler(message):
    su.last_name_handler(message, bot)

@bot.callback_query_handler(func=lambda call: call.data.startswith('su: '))
def sign_up_query(call):
    su.handle_query(bot, call.data, call.from_user.id)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: su.get_step_user_id(message.chat.id) == 6)
def last_name_handler(message):
    su.occupation_handler(message, bot)

@bot.message_handler(func=lambda message: su.get_step_user_id(message.chat.id) == 8)
def last_name_handler(message):
    su.phone_handler(message, bot)

@bot.message_handler(func=lambda message: su.get_step_user_id(message.chat.id) == 9)
def last_name_handler(message):
    su.how_met_handler(message, bot, db)
# SIGN UP ENDED

@bot.message_handler(commands=['users_list'])
def show_users_list_cmd(message):
    um.show_all_users(db, bot, message)

if __name__ == '__main__':
    db.setup()
    while True:
        try:
            bot.infinity_polling()
        except:
            pass