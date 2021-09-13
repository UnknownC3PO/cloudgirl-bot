import os
import json

if not os.path.isfile('users_db.json'):
    with open('users_db.json', 'w') as db:
        json.dump({'users': []}, db)


def check_key(data_users, user_id):
    for user in data_users['users']:
        if user_id == int(*user.keys()):
            return False
    return True


def get_user(user_id, city):
    try:
        with open('users_db.json', 'r+') as db_get:
            data_users = json.load(db_get)
            if check_key(data_users, user_id):
                data_users['users'].append({user_id: city})
                db_get.seek(0)
                json.dump(data_users, db_get)
                db_get.truncate()
                return True
    except NameError:
        return False


def del_user(user_id, city):
    try:
        with open('users_db.json', 'r+') as user_remove:
            data_users = json.load(user_remove)
            user_remove.seek(0)
            data_users['users'].remove({str(user_id): city})
            json.dump(data_users, user_remove)
            user_remove.truncate()
        return 'Deleted.'
    except ValueError:
        return 'Wrong city or your city not in list. Try again!'
