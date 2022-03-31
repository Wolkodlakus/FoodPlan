import states
import checks
import keyboards
from textwrap import dedent


def add_current_phone(update, context):
    update.message.reply_text(
        dedent(f'''\
        Ваш номер телефона {update.message.contact.phone_number } сохранен.
        Введите вашу фамилию:''')
    )
    print('We need to add current user phone in the db')
    return states.States.INPUT_USER_SURNAME


def input_new_phone(update, context):
    update.message.reply_text(
        dedent('''\
        Введите свой номер телефона.
        Принимаются номера только Российских операторов, \
        состоящие из 11 цифр, включая код страны.
        Номер надо вводить через +7.
        Пример: +7 911 111 22 33''')
    )
    return states.States.INPUT_NEW_PHONE


def add_new_phone(update, context):
    phone = update.message.text

    if not checks.check_phone(phone):
        update.message.reply_text(
            dedent(f'''\
            Вы ввели некорректный номер телефона.
            Вы ввели: {phone}
            Попробуйте еще раз.''')
        )
        return states.States.INPUT_NEW_PHONE

    print('We need to add user phone in the db')

    update.message.reply_text(
        'Введите свою фамилию.'
    )

    return states.States.INPUT_USER_SURNAME


def input_surname(update, context):
    surname = update.message.text
    if not checks.check_ru_letters(surname):
        update.message.reply_text(
            dedent(f'''\
            Вы ввели некорректную фамилию. Используйте только кириллицу.
            Вы ввели: {surname}
            Попробуйте еще раз.''')
        )
        return states.States.INPUT_USER_SURNAME

    print('We need to save user surname in the db')

    update.message.reply_text(
        'Введите ваше Имя:'
    )
    return states.States.INPUT_USER_NAME


def input_name(update, context):
    name = update.message.text
    if not checks.check_ru_letters(name):
        update.message.reply_text(
            dedent(f'''\
            Вы ввели некорректное имя. Используйте только кириллицу.
            Вы ввели: {name}
            Попробуйте еще раз.''')
        )
        return states.States.INPUT_USER_NAME

    print('We need to save user name in the db')

    update.message.reply_text(
        'Информация о вас записана.',
        reply_markup=keyboards.create_personal_area()
    )
    return states.States.PERSONAL_AREA
