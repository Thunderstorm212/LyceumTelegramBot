import db
from datetime import datetime
# from assets import
import threading
from datetime import datetime, timedelta



def present(telegram_id, telegram_user):
    query = {"info.telegram_id": telegram_id}
    update_attendance = {"$set": {f"status.attendance": 2}}
    user = db.users_collection.find_one(query)
    if user is not None:
        user_status_data = user['status']
        user_attendance = user_status_data["attendance"]

        if user_attendance <= 1 and user_attendance != 2:
            if datetime.today().weekday() < 5:
                db.users_collection.update_one(user, update_attendance)
                print(f"User: {telegram_user} update attendance status; Set: ✅;")
                return True
            else:
                return "Holiday"

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


def nz_registration(telegram_id):
    pass


def my_marks(telegram_id, telegram_user):
    query = {"info.telegram_id": telegram_id}
    user = db.users_collection.find_one(query)
    if user is not None:
        marks = user['marks']
        marks_login = marks["login"]
        print(marks_login)
        if marks_login is not None:
            print(marks_login, "Not None")
        else:
            return None


def visiting(telegram_id, telegram_user, result_queue):
    query = {"info.telegram_id": telegram_id}
    user = db.users_collection.find_one(query)

    if user is not None:
        status = user['status']
        absence = status["absence"]
        if len(absence) > 0:
            start_date = datetime(2023, 9, 4) #start date
            end_date = datetime.today()

            date_list = [
                start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)
            ]
            date_list = [
                date_str for date_str in date_list if date_str.weekday() not in [5, 6]
            ]
            date_list = [
                x.strftime("%Y/%m/%d") for x in date_list
            ]

            list_visiting = list(set(date_list) - set(absence))

            percentage_visiting = (len(list_visiting) / len(date_list)) * 100 if len(date_list) != 0 else 0

            result_queue.put((absence, round(percentage_visiting, 2)))

        else:
            result_queue.put((None, 100))

    else:
        result_queue.put(False)
