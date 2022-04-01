from telegram import KeyboardButton, ReplyKeyboardMarkup


def make_reply_markup(keyboard):
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_user_phone():
    keyboard = [
        [KeyboardButton(text='SEND', request_contact=True)],
        [KeyboardButton(text='ADD')],
    ]
    return make_reply_markup(keyboard)


def create_personal_area():
    keyboard = [
        [KeyboardButton(text='Мои подписки')],
        [KeyboardButton(text='Создать подписку')],
    ]
    return make_reply_markup(keyboard)

