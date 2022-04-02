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


def get_one_subscription():
    keyboard = [
        [KeyboardButton(text='Мои подписки')],
        [KeyboardButton(text='Создать подписку')],
    ]
    return make_reply_markup(keyboard)


def create_all_subscriptions_keyboards(subscriptions):
    keyboard = [[KeyboardButton(text=sub)] for sub in subscriptions]
    return make_reply_markup(keyboard)


def choose_menu_type():
    keyboard = [
        [KeyboardButton(text='Классическое')],
        [KeyboardButton(text='Низкоуглеводное')],
        [KeyboardButton(text='Вегетарианское')],
        [KeyboardButton(text='Кето')],
    ]
    return make_reply_markup(keyboard)


def choose_allergies():
    keyboard = [
        [KeyboardButton(text='Нет')],
        [KeyboardButton(text='Рыба и морепродукты')],
        [KeyboardButton(text='Мясо')],
        [KeyboardButton(text='Зерновые')],
        [KeyboardButton(text='Продукты пчеловодства')],
        [KeyboardButton(text='Орехи и бобовые')],
        [KeyboardButton(text='Молочные продукты')],
    ]
    return make_reply_markup(keyboard)


def choose_subscriptions_term():
    keyboard = [
        [KeyboardButton(text='1')],
        [KeyboardButton(text='3')],
        [KeyboardButton(text='6')],
        [KeyboardButton(text='12')],
    ]
    return make_reply_markup(keyboard)


def pay():
    keyboard = [
        [KeyboardButton(text='PAY')],
    ]
    return make_reply_markup(keyboard)
