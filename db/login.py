import db
from assets import parser
import threading
from queue import Queue


def verification_user(telegram_id, number):
    # print("number", number, "id", telegram_id)
    query = {"info.number": number}
    update = {"$set": {f"info.telegram_id": telegram_id}}

    user = db.users_collection.find_one(query)

    if user is not None:
        user_info_data = user['info']
        telegram_id = user_info_data['telegram_id']
        if telegram_id is None:
            db.users_collection.update_one(user, update)
        return True
    else:
        return False


def verification_user_from_login(telegram_id, login):
    query = {"info.login": login}
    update = {"$set": {f"info.telegram_id": telegram_id}}

    user = db.users_collection.find_one(query)
    if user is not None:
        user_info_data = user['info']
        telegram_id = user_info_data['telegram_id']
        if telegram_id is None:
            db.users_collection.update_one(user, update)
        return True
    else:
        return False


def verification_user_with_id(telegram_id):
    query = {"info.telegram_id": telegram_id}
    user = db.users_collection.find_one(query)
    if user is not None:
        return True
    else:
        return False


def verification_user_journal(telegram_id, result_queue):
    query = {"info.telegram_id": telegram_id}
    user = db.users_collection.find_one(query)
    if user is not None:
        marks = user['marks']
        marks_login = marks["login"]
        if marks_login is not None:
            marks_password = marks["password"]
            result_queue.put((marks_login, marks_password))
        elif marks_login is None:
            result_queue.put((None, None))
        else:
            result_queue.put(False)


def login_in_journal(telegram_id, login, password, result_queue):
    query = {"info.telegram_id": telegram_id}
    update = {
        "$set": {
            f"marks.login": login,
            f"marks.password": password
        }
    }

    user = db.users_collection.find_one(query)
    result = parser.open_driver(login, password, user)
    if result:
        if user is not None:
            db.users_collection.update_one(user, update)
            # db.users_collection.update_one(user, update_password)


            result_queue.put(result)
    else:
        result_queue.put(result)
        print("result:", result)



    # query = {"info.telegram_id": telegram_id}
    # user = db.users_collection.find_one(query)
