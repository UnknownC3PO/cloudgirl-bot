import os
import json
import logging

if not os.path.isfile('users_db.json'):
    with open('users_db.json', 'w') as db:
        json.dump({'users': []}, db)


def get_user(user_id):
    with open('users_db.json', 'r') as db_get:
        data_users = json.load(db_get)
    for user in data_users['users']:
        if user_id == user['id']:
            return str(user)
    return None


def add_user(user_id, city):
    try:
        with open('users_db.json', 'r+') as db_add:
            data_users = json.load(db_add)
            for user in data_users['users']:
                if user_id == user['id']:
                    return False
            data_users['users'].append({'id': int(user_id), 'city': city})
            db_add.seek(0)
            json.dump(data_users, db_add)
            db_add.truncate()
            return True
    except NameError:
        logging.exception('UserError')


def del_user(user_id, city):
    try:
        with open('users_db.json', 'r+') as user_remove:
            data_users = json.load(user_remove)
            data_users['users'].remove({'id': user_id, 'city': str(city)})
            user_remove.seek(0)
            json.dump(data_users, user_remove)
            user_remove.truncate()
        return True
    except ValueError:
        logging.exception('UserError')


def update_user(user_id, city):
    try:
        with open('users_db.json', 'r+') as user_update:
            data_users = json.load(user_update)
            for user in data_users['users']:
                if user_id == user['id']:
                    data_users['users'].remove({'id': user_id, 'city': user['city']})
                    data_users['users'].append({'id': int(user_id), 'city': city})
                    user_update.seek(0)
                    json.dump(data_users, user_update)
                    user_update.truncate()
                    return True
    except ValueError:
        logging.exception('UserError')
