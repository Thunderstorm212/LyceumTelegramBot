import telegram
from telegram import Update, Contact
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import json
import conf
from assets.ui import ui_text
from db import menager, login
import db
import threading


class ChatData:
    def __init__(self):
        self.chat_data_file = open("conf/chats_data.json")
        # chat_data = json.dump(, sort_keys = True, indent = 4)

    def add(self, obj_id:str, input_data):
        file_data = dict(json.load(self.chat_data_file))
        obj_id = obj_id.split(".")

        def change_value(obj, target_key, new_value):
            for key in obj:
                if key == target_key:
                    obj[key] = new_value
                elif isinstance(obj[key], dict):
                    change_value(obj[key], target_key, new_value)

        change_value(file_data[obj_id[0]], obj_id[-1], input_data)
        json_file = json.dumps(file_data, sort_keys=True, indent=2, ensure_ascii=False)
        open("conf/chats_data.json", "w+").write(json_file)

    def add_obj(self, input_data: dict):
        pass
        file_data = dict(json.load(self.chat_data_file))
        print("file data", file_data)
        for key, val in input_data.items():
            file_data[key] = val

        json_file = json.dumps(file_data, sort_keys=True, indent=2, ensure_ascii=False)
        open("conf/chats_data.json", "w+").write(json_file)

    def get(self):
        return json.load(self.chat_data_file)

    def get_by_id(self, obj_id: str):
        file_data = dict(json.load(self.chat_data_file))
        obj_id = obj_id.split(".")
        try:
            for key in obj_id:
                file_data = file_data[key]
            return file_data
        except (KeyError, TypeError):
            return None



class Buttons:
    numberBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_number, request_contact=True),
        ]
    ]

    homeBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_home),
            telegram.KeyboardButton(ui_text["btn"].btn_stats),
        ],
        [
            telegram.KeyboardButton(ui_text["btn"].btn_visiting),
            telegram.KeyboardButton(ui_text["btn"].btn_menu),
        ]
    ]
    visitingBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_arrived),
            telegram.KeyboardButton(ui_text["btn"].btn_intheway),
            telegram.KeyboardButton(ui_text["btn"].btn_back),
        ]
    ]
    statusBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_marks_status),
            telegram.KeyboardButton(ui_text["btn"].btn_visiting_status),
            telegram.KeyboardButton(ui_text["btn"].btn_back),
        ]
    ]


class Bot(Buttons):
    @staticmethod
    async def star_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

        contact_user_id = update.message.chat_id
        user_name = update.message.from_user

        if login.verification_user_with_id(contact_user_id):
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].answer_login_confirmed,
                                           reply_markup=markup)
            chat_data_query = {
                str(contact_user_id): {
                    "info": {},
                    "dev_mode": False
                }
            }
            if ChatData().get_by_id(str(contact_user_id)) is None:
                ChatData().add_obj(chat_data_query)
        else:
            markup = telegram.ReplyKeyboardMarkup(Buttons.numberBTN, resize_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].answer_start, reply_markup=markup)

    @staticmethod
    async def dev_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.args[0] == "1486" and update.message.chat_id in conf.dev_info:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="розробник підтверджений")

    @staticmethod
    async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
        contact = update.message.contact
        contact_user_id = contact.user_id
        contact_phone_number = contact.phone_number.replace("+", "")
        if login.verification_user(contact_user_id, contact_phone_number):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].answer_login_confirmed)
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["btn"].btn_home,
                reply_markup=markup
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].answer_login_not_confirmed)

    @staticmethod
    async def all_responses(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message.text
        user = update.message.from_user
        user_name = user.first_name
        user_id = user.id

        if message == ui_text["btn"].btn_back:
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["btn"].btn_home,
                reply_markup=markup
            )

        if message == ui_text["btn"].btn_visiting:
            markup = telegram.ReplyKeyboardMarkup(Buttons.visitingBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["btn"].btn_visiting,
                reply_markup=markup
            )

        if message == ui_text["btn"].btn_stats:
            markup = telegram.ReplyKeyboardMarkup(Buttons.statusBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["btn"].btn_stats,
                reply_markup=markup
            )

        if message == ui_text["btn"].btn_intheway:
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)

            if db.status.in_the_way(update.message.chat_id, user_name):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=ui_text["answer"].answer_info,
                    reply_markup=markup
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=ui_text["answer"].answer_status_updated,
                    reply_markup=markup
                )

        if message == ui_text["btn"].btn_arrived:
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            if db.status.present(update.message.chat_id, user_name):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=ui_text["answer"].answer_info,
                    reply_markup=markup
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=ui_text["answer"].answer_status_updated,
                    reply_markup=markup
                )


