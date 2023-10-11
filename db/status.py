import db
from datetime import datetime


def present(telegram_id):
    query = {"info.telegram_id": telegram_id}
    update = {"$set": {f"status.attendance": 2}}
    user = db.users_collection.find_one(query)
    # print(user)
    if user is not None:
        user_status_data = user['status']
        user_attendance = user_status_data["attendance"]
        if user_attendance <= 1:
            db.users_collection.update_one(user, update)

        print(week_number_in_month(datetime.now()))

        return True
    else:
        return False


def in_the_way(telegram_id):
    query = {"info.telegram_id": telegram_id}
    update = {"$set": {f"status.attendance": 1}}
    user = db.users_collection.find_one(query)
    # print(user)
    if user is not None:
        user_status_data = user['status']
        user_attendance = user_status_data["attendance"]
        if user_attendance <= 1:
            db.users_collection.update_one(user, update)

        print(week_number_in_month(datetime.now()))

        return True
    else:
        return False

def week_number_in_month(dt):
  cur_date = datetime.now()

  start_date = datetime(2023, 9, 4)
  data = cur_date.strftime('%Y/%m/%d %H:%M')
  print(data)
  # data ]= datetime.strptime()
  # print(data)
  # current_date = datetime(data.year, data.month, data.day)
  # delta = current_date - start_date
  #
  # weeks = delta.days / 7
  # return int(weeks % 4) + 1

