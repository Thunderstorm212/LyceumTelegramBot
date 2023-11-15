from pymongo.mongo_client import MongoClient
from conf import DB_TOKEN, DB_USER
import csv
import json


cluster = "cluster0"
uri = f"mongodb+srv://{DB_USER}:{DB_TOKEN}@{cluster}.gbcrwrb.mongodb.net/?retryWrites=true&w=majority"
# test_client = MongoClient('mongodb://localhost:27017/')
client = MongoClient(uri)
customer_db = client["customer"]
users_collection = customer_db["users"]

csvfile = open('lib/Users.csv', 'r', newline='')
csvreader = csv.reader(csvfile)
logins_data = [row[1] for row in csvreader]
logins_data = logins_data[1:]

csvfile = open('lib/Users.csv', 'r', newline='')
csvreader = csv.reader(csvfile)
numbers_data = [row[2] for row in csvreader]
numbers_data = numbers_data[1:]

csvfile = open('lib/Users.csv', 'r', newline='')
csvreader = csv.reader(csvfile)
email_data = [row[6] for row in csvreader]
email_data = email_data[1:]

csvfile = open('lib/Users.csv', 'r', newline='')
csvreader = csv.reader(csvfile)
full_name_data = [row[3] for row in csvreader]
full_name_data = full_name_data[1:]

csvfile = open('lib/Users.csv', 'r', newline='')
csvreader = csv.reader(csvfile)
group_data = [row[4] for row in csvreader]
group_data = group_data[1:]
group_result = list()
for group in group_data:
    group = int(group)
    if group == 0:
        group_result.append("10A")
    if group == 1:
        group_result.append("10Б")
    if group == 2:
        group_result.append("10В")
    if group == 3:
        group_result.append("10Г")
group_data = group_result



# marks = None


class User:
    users = list()
    def build_user(self, number, full_name, absence, login, email, group, attendance=0, telegram_id=None):
        user = {
             "info": {
                "number": number,
                "telegram_id": telegram_id,
                "full_name": full_name,
                "login": login,
                "email": email,
                "group": group,

             },
             "status": {
                 "attendance": attendance,
                 "absence": absence,
             },
             "marks": {

             }


        }
        self.users.append(user)

    def get_all_users(self):
        return self.users


user = User()

for i in range(len(logins_data)):
    user.build_user(
        number=numbers_data[i],
        full_name=full_name_data[i],
        login=logins_data[i],
        email=email_data[i],
        group=group_data[i],
        absence=[]
    )
# users_result = dict()
#
# for user_dict in user.get_all_users():
#     users_result.update(user_dict)

# print(users_result)

# users_collection.insert_many(user.get_all_users())
print(customer_db.command('ping'))
