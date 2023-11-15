import db


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


def verification_user_with_id(telegram_id):
    query = {"info.telegram_id": telegram_id}
    user = db.users_collection.find_one(query)
    if user is not None:
        return True
    else:
        return False
