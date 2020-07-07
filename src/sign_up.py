from telebot import types

def get_field_by_step_sign_up(step):
    if step == 1:
        return "ready"
    if step == 2:
        return "email"
    if step == 3:
        return "first_name"
    if step == 4:
        return 'last_name'
    if step == 5:
        return 'has_participated'
    if step == 6:
        return 'is_phone'
    if step == 7:
        return 'occupation'
    if step == 8:
        return 'has_17'
    if step == 9:
        return 'phone'
    if step == 10:
        return 'how_met'

class SignUpModel:
    def __init__(self):
        self.a = 'b'
        self.sign_up_context = {
            "something": {}
        }
        self.sign_up_steps = {
            "something": {}
        }

    def set_step_and_info(self, user_id, step, value):
        if str(user_id) not in self.sign_up_context:
            self.sign_up_context[str(user_id)] = {}

        self.sign_up_context[str(user_id)][get_field_by_step_sign_up(step)] = value
        self.sign_up_steps[str(user_id)] = step

    def get_step_user_id(self, user_id):
        if str(user_id) not in self.sign_up_steps:
            return 0
        return self.sign_up_steps[str(user_id)]

    def get_entire_user_info(self, user_id):
        return self and self.sign_up_context and self.sign_up_context[str(user_id)]

    def reset_user_info(self, user_id, status = 0):
        if not status:
            if self and self.sign_up_context and self.sign_up_context[str(user_id)]:
                self.sign_up_context[str(user_id)] = {}
            if self and self.sign_up_steps and self.sign_up_steps[str(user_id)]:
                self.sign_up_steps[str(user_id)] = 0
        else:
            if self and self.sign_up_context and self.sign_up_context[str(user_id)]:
                self.sign_up_context[str(user_id)] = {}
                self.set_step_and_info(user_id, 1, True)

    def sign_up_cmd_handler(self, message, bot):
        cid = message.chat.id
        msg = bot.send_message(cid, "Привет, безумно рад, что ты хочешь к нам присоединиться! \n\n"
                              "Для начала напиши мне <b>адрес своей электронной почты: </b>",
                         parse_mode="HTML")
        self.set_step_and_info(cid, 1, True)
        a = self.get_step_user_id(cid)

    def email_handler(self, message, bot):
        cid = message.chat.id
        self.set_step_and_info(cid, 2, message.text)
        bot.send_message(cid, "Электронную почту я запомнил :) \n"
                                     "Теперь введи свое <b>имя</b>! \n\n"
                                     "<i>Например: Юлия, Александр</i>", parse_mode="HTML")

    def first_name_handler(self, message, bot):
        cid = message.chat.id
        self.set_step_and_info(cid, 3, message.text)
        bot.send_message(cid, "Какое прекрасное имя!\n"
                                  "Теперь введи <b>фамилию</b>\n\n"
                                  "<i>Например: Иванова, Сидоров</i>", parse_mode="HTML")

    def last_name_handler(self, message, bot):
        cid = message.chat.id
        self.set_step_and_info(cid, 4, message.text)
        bot.send_message(cid, "Повезло твоей семье.\n"
                                  "Фамилию тоже запомнил!", parse_mode="HTML")

        mk = types.InlineKeyboardMarkup()
        mk.row(types.InlineKeyboardButton('Да, хочу еще', callback_data="su: 5 T"))
        mk.row(types.InlineKeyboardButton('Нет, хочу попробовать', callback_data="su: 5 F"))
        bot.send_message(cid, "Участвовал ли ты раньше?", reply_markup=mk)

    def occupation_handler(self, message, bot):
        cid = message.chat.id
        self.set_step_and_info(cid, 7, message.text)

        mk = types.InlineKeyboardMarkup()
        mk.row(types.InlineKeyboardButton('Да', callback_data="su: 8 T"))
        mk.row(types.InlineKeyboardButton('Нет', callback_data="su: 8 F"))
        bot.send_message(cid, "На момент участия в мероприятии тебе уже будет 17 лет?", reply_markup=mk)

    def phone_handler(self, message, bot):
        cid = message.chat.id
        self.set_step_and_info(cid, 9, message.text)

        bot.send_message(cid, "Обещаю не звонить по пустякам!")
        bot.send_message(cid, "А как ты о нас узнал?\n"
                                     "<i>Например: Прочитал в новостях, подсказал знакомый</i>", parse_mode="HTML")

    def how_met_handler(self, message, bot, db):
        cid = message.chat.id
        self.set_step_and_info(cid, 10, message.text)

        sign_up_info = self.get_entire_user_info(cid)
        db.add_user({
            "id": message.from_user.id,
            "first_name": sign_up_info['first_name'],
            "last_name": sign_up_info['last_name'],
            "username": message.from_user.username,
            "email": sign_up_info['email'],
            "has_participated": int(sign_up_info['has_participated'] == "True"),
            "is_phone": int(sign_up_info['is_phone'] == "True"),
            "occupation": sign_up_info['occupation'],
            "has_17": int(sign_up_info['has_17'] == "True"),
            "phone": sign_up_info['phone'],
            "how_met": sign_up_info['how_met'],
        })
        self.reset_user_info(cid, 0)
        bot.send_message(cid, sign_up_info)
        bot.send_message(cid, "<b>Регистрация прошла успешно!</b>\n"
                                  "Спасибо большое за знакомство:) Мне очень приятно!", parse_mode="HTML")

    def handle_query(self, bot, data, user_id):
        [_, op, val] = data.split(' ')
        if int(op) == 5:
            self.set_step_and_info(user_id, 5, str(val == "T"))
            bot.send_message(user_id, "Надеюсь, мы еще с тобой увидимся!")
            mk = types.InlineKeyboardMarkup()
            mk.row(types.InlineKeyboardButton('Телефон', callback_data="su: 6 T"))
            mk.row(types.InlineKeyboardButton('Фотоаппарат', callback_data="su: 6 F"))
            bot.send_message(user_id, "На что будешь фотографировать?", reply_markup=mk)
        if int(op) == 6:
            self.set_step_and_info(user_id, 6, str(val == "T"))
            bot.send_message(user_id, "Отличный выбор!")
            bot.send_message(user_id, "А где ты <b>учишься/работаешь?</b>\n"
                                         "<i>Например, БГУ ФПМИ, 4 курс\nДоминос, пиццамейкер</i>", parse_mode="HTML")
        if int(op) == 8:
            self.set_step_and_info(user_id, 8, str(val == "T"))
            bot.send_message(user_id, "Круто!\n"
                                         "Укажи, пожалуйста, номер <b>телефона</b>, по которому с тобой можно связаться\n\n"
                                         "<i>Например: +375295648756</i>", parse_mode="HTML")