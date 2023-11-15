import db
from datetime import datetime


def present(telegram_id, telegram_user):
    query = {"info.telegram_id": telegram_id}
    update = {"$set": {f"status.attendance": 2}}
    user = db.users_collection.find_one(query)
    if user is not None:
        user_status_data = user['status']
        user_attendance = user_status_data["attendance"]
        if user_attendance <= 1 and user_attendance != 2:
            db.users_collection.update_one(user, update)
            print(f"User: {telegram_user} update attendance status; Set: ✅;")
            return True
        else:
            return False

    else:
        print(f"User: {telegram_user} not update attendance status")

        return False


def in_the_way(telegram_id, telegram_user):
    query = {"info.telegram_id": telegram_id}
    update = {"$set": {f"status.attendance": 1}}
    user = db.users_collection.find_one(query)
    if user is not None:
        user_status_data = user['status']
        user_attendance = user_status_data["attendance"]
        if user_attendance <= 1:
            db.users_collection.update_one(user, update)
            print(f"User: {telegram_user} update attendance status; Set: 🚗;")
            return True
        else:
            return False
    else:
        print(f"User: {telegram_user} not update attendance status")
        return False