import datetime
import db
import time


def update_date():
    next_date = datetime.datetime.today() + datetime.timedelta(days=1)
    next_date = next_date.strftime('%Y/%m/%d')
    while True:
        today_date = datetime.datetime.today().strftime('%Y/%m/%d')
        print("Date is Update")
        if today_date == next_date and datetime.datetime.today().weekday() < 5:
            cursor = db.users_collection.find({})
            for document in cursor:
                status = document["status"]
                attendance = status["attendance"]

                if attendance > 0:
                    info = document["info"]
                    person = info["full_name"]

                    update_status = {"$set": {f"status.attendance": 0}}
                    db.users_collection.update_one(document, update_status)
                    print(f"Log: update {person} status attendance; Set: 0;")
                else:
                    info = document["info"]
                    person = info["full_name"]
                    telegram_id = info["telegram_id"]
                    if telegram_id is not None:
                        update_visiting = {"$push": {f"status.absence": today_date}}
                        db.users_collection.update_one(document, update_visiting)
                        print(f"Log: update {person} status absence; Push: {today_date};")

            time.sleep(28800)
            update_date()
        time.sleep(7200)

