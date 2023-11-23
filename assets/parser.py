from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import db
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os


class Elements:

    id = {
        "input_login": "loginform-login",
        "input_password": "loginform-password",
        "date_from": "classselectform-date_from",
        "date_to": "classselectform-date_to"
    }
    class_name = {
        "btn_submit": "form-submit-btn"
    }


driver = None


def open_driver(login, password, user=None):

    global driver

    def login_client():
        driver.get("https://nz.ua")
        input_login = driver.find_element(by=By.ID, value=Elements.id["input_login"])
        input_password = driver.find_element(by=By.ID, value=Elements.id["input_password"])
        submit_btn = driver.find_element(by=By.CLASS_NAME, value=Elements.class_name["btn_submit"])
        input_login.send_keys(login)
        input_password.send_keys(password)

        submit_btn.click()
        sleep(1)
        try:
            driver.find_element(by=By.CLASS_NAME, value="alert-danger")
            return False
        except Exception as ex:
            return True

    def get_marks():
        driver.get("https://nz.ua/schedule/grades-statement")
        data = []
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        list_header = []
        header = soup.find_all("table")[0].find("tr")

        for items in header:
            try:
                if items == "\n":
                    pass
                else:
                    list_header.append(items.get_text())
            except Exception as ex:
                print(ex)
                continue
        html_data = soup.find_all("table")[0].find_all("tr")[1:]
        for element in html_data:
            sub_data = []
            for sub_element in element:
                try:
                    if sub_element == "\n":
                        pass
                    else:
                        sub_data.append(sub_element.get_text())
                except Exception as ex:
                    print(ex)
                    continue
            data.append(sub_data)

        data_frame = pd.DataFrame(data=data, columns=list_header)
        sleep(1)
        data_frame.to_csv(f'lib/marks/Marks_{login}.csv')

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
                                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON
                                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object
                                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
                                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy
                                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
                                '''
        })

        if login_client() is False:
            return False
        get_marks()

        csv_file = f'lib/marks/Marks_{login}.csv'
        marks_list = parse_csv(csv_file)
        if user is not None:
            current_date = datetime.today().strftime('%Y/%m/%d')
            update = {
                "$push": {
                    f"marks.marks": {'$each': marks_list}
                },
                "$set": {
                    "marks.last_update": current_date,
                    "marks.login": login,
                    "marks.password": password
                }
            }
            db.users_collection.update_one(user, update)
        os.remove(csv_file)
        return True
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def parse_csv(input_csv):
    # Open CSV file for reading
    with open(input_csv, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        subjects_data = [row[2] for row in csvreader]
        subjects_data = subjects_data[1:]

    with open(input_csv, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        marks_data = [row[3] for row in csvreader]
        marks_data = marks_data[1:]

    result = []
    for subject, details in zip(subjects_data, marks_data):
        result.append([subject, details])
    return result
