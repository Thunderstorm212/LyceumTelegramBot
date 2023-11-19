from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas

from bs4 import BeautifulSoup
import pandas as pd
from threading import Thread
import csv


class LoginData:
    login_data = "gaydaychuk_vladislav2"
    password_data = "676526dd"


elements_id = {
    "input_login": "loginform-login",
    "input_password": "loginform-password",
    "date_from": "classselectform-date_from",
    "date_to": "classselectform-date_to"
}

elements_data = {
    "input_login": LoginData.login_data,
    "input_password": LoginData.password_data,
}


def open_driver():

    def login_client():
        driver.get("https://nz.ua")

        input_login = driver.find_element(by=By.ID, value=elements_id["input_login"])
        input_password = driver.find_element(by=By.ID, value=elements_id["input_password"])
        submit_btn = driver.find_element(by=By.CLASS_NAME, value="form-submit-btn")
        input_login.send_keys(elements_data["input_login"])
        input_password.send_keys(elements_data["input_password"])

        submit_btn.click()

        sleep(1)

    def get_marks():
        driver.get("https://nz.ua/schedule/grades-statement")
        sleep(3)
        data = []
        html = driver.page_source
        soup = BeautifulSoup(html)
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
        HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
        for element in HTML_data:
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

        dataFrame = pd.DataFrame(data=data, columns=list_header)
        dataFrame.to_csv('Marks.csv')

        from_date = driver.find_element(by=By.ID, value=elements_id["date_from"])
        print(from_date.get_property)

    try:
        # driver = connect_driver()
        # login_client()
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        s = Service(executable_path="../lib/chrome_service/chromedriver")

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

        # get_marks()
        thread1 = Thread(target=login_client)
        thread2 = Thread(target=get_marks)


        thread1.start()
        thread1.join()
        sleep(1)
        thread2.start()
        thread2.join()

    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


open_driver_thread = Thread(target=open_driver)

open_driver_thread.start()
open_driver_thread.join()


def csv_to_pdf(input_csv, output_pdf):
    fontname = "Roboto-Medium"
    fontfile = "../lib/Roboto-Medium.ttf"
    doc = SimpleDocTemplate("Schedule.pdf", pagesize=(612, 1200), topMargin=10)
    elements = []
    pdfmetrics.registerFont(TTFont(fontname, fontfile))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomFont', fontName=fontname, fontSize=15))

    header_data = ["№", "Предмет", "Оцінки"]
    # Open CSV file for reading
    with open('Marks.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        subjects_data = [row[2] for row in csvreader]
        subjects_data = subjects_data[1:]
        # print(subjects_data)

    with open('Marks.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        marks_data = [row[3] for row in csvreader]
        marks_data = marks_data[1:]

        # print(marks_data)

    result = []
    for subject, details in zip(subjects_data, marks_data):
        result.append([subject, details])

    # elements.append(Paragraph(date, styles['CustomFont']))

    print(result)




    table = Table()

    table_style = [
        ('FONTNAME', (0, 0), (-1, -1), fontname),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E7EAEF"))
    ]
    table.setStyle(TableStyle(table_style))

    elements.append(Spacer(1, 12))
    elements.append(table)
    elements.append(Spacer(1, 12))

        # # Set initial y-coordinate for drawing on the PDF
        # y = 800
        #
        # for row in csv_reader:
        #     # Write each row to the PDF
        #     for item in row:
        #         pdf.drawString(100, y, item)
        #         y -= 12  # Adjust y-coordinate for the next line
        #
        #     y -= 20  # Add some space between rows
        #
        # # Save the PDF
        # pdf.save()
    # Create a PDF document
    doc.build(elements)

#
# input_csv_file = 'Marks.csv'
# output_pdf_file = 'output.pdf'
# csv_to_pdf(input_csv_file, output_pdf_file)
#
# def create_pdf():
#     # c = canvas.Canvas("simple_pdf.pdf")
#     elements = []
#     csvfile = open('Marks.csv', 'r', newline='')
#     csvreader = csv.reader(csvfile)
#     cvs_data = [row[1] for row in csvreader]
#     cvs_data = cvs_data[1:]
#     print(cvs_data)
#
#
#     data = [[]]
#     # pdfmetrics.registerFont(TTFont(fontname, fontfile))
#     doc = SimpleDocTemplate("test.pdf", pagesize=(612, 1200), topMargin=10)
#     styles = getSampleStyleSheet()
#     # styles.add(ParagraphStyle(, fontSize=16))
#     table_data = [["№", "Предмет", "Вчитель", "Аудиторія", "Підгрупа"]]
#     # for lesson in day:
#     #     table_data.append(lesson)
#     col_widths = [20, 150, 170, 70, 70]  # Задайте ширину каждого столбца здесь
#     table = Table(table_data, colWidths=col_widths)
#     elements.append(table)
#     doc.build(elements)
# #
# create_pdf()


