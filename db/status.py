import db
from datetime import datetime, timedelta
import conf


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
                print(f"User: {telegram_user} not update attendance status")
                return "Holiday"

        else:
            print(f"User: {telegram_user} not update attendance status")
            return False
    else:

        return False


def in_the_way(telegram_id, telegram_user):
    query = {"info.telegram_id": telegram_id}
    update = {"$set": {f"status.attendance": 1}}
    user = db.users_collection.find_one(query)
    if user is not None:
        user_status_data = user['status']
        user_attendance = user_status_data["attendance"]
        if user_attendance < 1 and user_attendance != 1:
            db.users_collection.update_one(user, update)
            print(f"User: {telegram_user} update attendance status; Set: 🚗;")
            return True
        else:
            print(f"User: {telegram_user} not update attendance status")
            return False
    else:
        return False


def my_marks(telegram_id, result_queue):
    query = {"info.telegram_id": telegram_id}
    user = db.users_collection.find_one(query)
    if user is not None:
        marks_obj = user['marks']
        marks_list = marks_obj["marks"]
        last_update = marks_obj["last_update"]

        if last_update is not None:
            days_difference = (datetime.now() - datetime.strptime(last_update, "%Y/%m/%d")).days
            print(days_difference)
            if days_difference >= 3:
                result_queue.put(None)
            else:
                text = f"📚️Оцінки: \n" \
                       f"⏰ {last_update}\n"
                for subject_data in marks_list:
                    subject = subject_data[0].replace('ІК "Природничі науки. ', "")
                    subject = subject.replace('"', "")
                    marks = subject_data[1].replace('(', "")
                    marks = marks.replace(')', "")
                    marks = marks.replace('.', "")
                    text = text + f"*{subject}*\:\n_{marks}_\n\n"
                result_queue.put(text)


def visiting(telegram_id, telegram_user, result_queue):
    query = {"info.telegram_id": telegram_id}
    user = db.users_collection.find_one(query)

    if user is not None:
        status = user['status']
        absence = status["absence"]
        if len(absence) > 0:
            start_date = conf.start_date_status  # start date
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

            print(f"User: {telegram_user} get visiting status")
            result_queue.put((absence, round(percentage_visiting, 2)))
        else:
            print(f"User: {telegram_user} get visiting status. Get: 100% visiting")
            result_queue.put((None, 100))
    else:
        result_queue.put(False)
