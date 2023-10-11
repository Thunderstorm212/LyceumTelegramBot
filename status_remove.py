from datetime import datetime
import time
import db
import calendar


def update_data():
    now_data = datetime.now().strftime('%Y/%m/%d %H:%M')
    today_data = datetime.today().strftime('%Y/%m/%d') + " 23:59"
    if now_data == today_data:
        print(today_data)

        # for i in  :
        # # db.users_collection.find_one()
    # print(db..find({}))
    cursor = db.users_collection.find({})
    for document in cursor:
        print(document)
        status = document["status"]
        attendance = status["attendance"]

        if attendance > 0:
            update = {"$set": {f"status.attendance": 0}}
            db.users_collection.update_one(document, update)
        else:
            pass
    print("data=", now_data)
    time.sleep(60)


# update_data()


def week_number_in_month():
    # calendar.setfirstweekday(calendar.SUNDAY)
    yy = int(datetime.now().strftime('%Y'))
    mm = int(datetime.now().strftime('%m'))
    dd = int(datetime.now().strftime('%d'))
    print(dd)
week_number_in_month()