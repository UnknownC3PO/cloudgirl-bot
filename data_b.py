import os
import json

users = {'users': []}


def get_all_keys(dict_users):
    keys = []
    try:
        for user in dict_users['users']:
            for key in user.items():
                keys.append(int(key[0]))
        return keys
    except KeyError:
        pass


def create_user(user_id, city):
    if not os.path.isfile('users_db.json'):
        users['users'].append({user_id: city})
        with open('users_db.json', 'w', encoding='utf-8') as db_cr:
            json.dump(users, db_cr)
        return 'Added.'
    else:
        with open('users_db.json', 'r', encoding='utf-8') as db_r:
            json_text = json.load(db_r)
        if (user_id not in get_all_keys(json_text)) or not json_text['users']:
            json_text['users'].append({user_id: city})
            with open('users_db.json', 'w', encoding='utf-8') as db_add:
                json.dump(json_text, db_add)
            return 'Added.'
        else:
            return 'User already exists.'


def del_user(user_id, city):
    try:
        with open('users_db.json', 'r', encoding='utf-8') as db_rdel:
            json_del = json.load(db_rdel)
        dl_user = {str(user_id): city}
        json_del['users'].remove(dl_user)
        with open('users_db.json', 'w', encoding='utf-8') as db__wdel:
            json.dump(json_del, db__wdel)
        return 'Deleted.'
    except ValueError:
        return 'Wrong city or your city not in list. Try again!'
