import datetime
import db
import time


def update_date():
    next_date = datetime.datetime.today() + datetime.timedelta(days=1)
    next_date = next_date.strftime('%Y/%m/%d')
    while True:
        today_date = datetime.datetime.now().strftime('%Y/%m/%d')
        print("Date is Update")
        if today_date == next_date:
            cursor = db.users_collection.find({})
            for document in cursor:
                status = document["status"]
                attendance = status["attendance"]

                if attendance > 0:
                    info = document["info"]
                    person = info["full_name"]

                    update = {"$set": {f"status.attendance": 0}}
                    db.users_collection.update_one(document, update)
                    print(f"Log: update {person} status attendance; Set: 0;")
                else:
                    pass
            time.sleep(28800)
            update_date()
        time.sleep(7200)

