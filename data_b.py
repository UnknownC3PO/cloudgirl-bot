import os
import json

if not os.path.isfile('users_db.json'):
    with open('users_db.json', 'w') as db:
        json.dump({'users': []}, db)


def check_key(data_users, user_id):
    for user in data_users['users']:
        if user_id == int(user['id']):
            return False
    return True


def get_user(user_id):
    with open('users_db.json', 'r') as db_get:
        data_users = json.load(db_get)
    for user in data_users['users']:
        if user_id == int(user['id']):
            return str(user['city'])
    return 'User does not exist.'


def add_user(user_id, city):
    try:
        with open('users_db.json', 'r+') as db_add:
            data_users = json.load(db_add)
            if check_key(data_users, user_id):
                data_users['users'].append({'id': user_id, 'city': city})
                db_add.seek(0)
                json.dump(data_users, db_add)
                db_add.truncate()
            return True
    except NameError:
        return False


def del_user(user_id, city):
    try:
        with open('users_db.json', 'r+') as user_remove:
            data_users = json.load(user_remove)
            user_remove.seek(0)
            data_users['users'].remove({'id': user_id, 'city': city})
            json.dump(data_users, user_remove)
            user_remove.truncate()
        return 'Deleted.'
    except ValueError:
        return 'Wrong city or your city not in list. Try again!'


def update_user(user_id, city):
    try:
        user_for_update = get_user(user_id)
        del_user(user_id, user_for_update)
        add_user(user_id, city)
        return 'Updated'
    except ValueError:
        return 'User does not exist.'
