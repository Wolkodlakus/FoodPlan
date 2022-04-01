from textwrap import dedent

import checks
import keyboards
import states
import funcs_db


def add_current_phone(update, context):
    phone_number = update.message.contact.phone_number
    context.chat_data['phone_number'] = phone_number
    update.message.reply_text(
        dedent(f'''\
        Ваш номер телефона {phone_number} сохранен.
        Введите вашу фамилию:''')
    )
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

    context.chat_data['phone_number'] = phone
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

    context.chat_data['surname'] = surname

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
    new_user = {
        'user_name': name,
        'user_surname': context.chat_data['surname'],
        'user_phone': context.chat_data['phone_number']
    }
    update.message.reply_text(
        dedent(f'''\
            Информация о вас записана:
            Имя: {new_user['user_name']}
            Фамилия: {new_user['user_surname']}
            Номер телефона: {new_user['user_phone']}'''),
        reply_markup=keyboards.create_personal_area()
    )
    funcs_db.add_client(
        update.message.chat_id,
        new_user['user_name'],
        new_user['user_phone']
    )
    return states.States.PERSONAL_AREA
