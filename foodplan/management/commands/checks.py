import phonenumbers
import foodplan.management.commands.funcs_db as funcs_db


def check_ru_letters(user_input):
    ru_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    only_ru_letters = [letter for letter in user_input.lower()
                       if letter in ru_alphabet]
    return only_ru_letters == list(user_input.lower())


def check_phone(phone):
    try:
        all_info_about_phone = phonenumbers.parse(phone)
        country_code = phonenumbers.region_code_for_number(all_info_about_phone)
        if country_code != 'RU':
            return False
        return phonenumbers.is_possible_number(all_info_about_phone)

    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def check_subscriptions(tg_id):
    db_user_id = funcs_db.find_client(tg_id)
    return funcs_db.get_client_subscriptions(db_user_id)

