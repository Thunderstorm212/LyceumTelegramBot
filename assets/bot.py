import datetime
import time

import telegram
from telegram import Update, Contact
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
import json
import conf
from assets.ui import ui_text
from db import menager, login
import db
import threading
from queue import Queue


class Buttons:
    loginBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_number, request_contact=True),
            telegram.KeyboardButton(ui_text["btn"].btn_login),

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
    # user = update.message.from_user
    # user_name = user.first_name
    # user_id = user.id


    @staticmethod
    def message_construct(context, update, text: str = None, parse: str = None,
                          markup: telegram.ReplyKeyboardMarkup = None):
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=markup,
            parse_mode=parse
        ).message_id

        return message

    @staticmethod
    async def star_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

        contact_user_id = update.message.chat_id
        context.user_data['id'] = contact_user_id

        user_name = update.message.from_user
        if login.verification_user_with_id(context.user_data['id']):
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_login_confirmed,
                reply_markup=markup,
                parse_mode="MarkdownV2",
            )
        else:
            markup = telegram.ReplyKeyboardMarkup(Buttons.loginBTN, resize_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].answer_start,
                                           parse_mode="MarkdownV2", reply_markup=markup)

    # @staticmethod
    # async def dev_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     if context.args[0] == "1486" and update.message.chat_id in conf.dev_info:
    #         await context.bot.send_message(chat_id=update.effective_chat.id, text="розробник підтверджений")

    @staticmethod
    async def registration_from_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
        contact = update.message.contact
        contact_phone_number = contact.phone_number.replace("+", "")
        if login.verification_user(context.user_data['id'], contact_phone_number):
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=ui_text["answer"].answer_login_confirmed, reply_markup=markup)

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].error_login_not_confirmed)

    @staticmethod
    async def registration_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_login,
                parse_mode="MarkdownV2",
        )

        return 1

    @staticmethod
    async def registration_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_login = update.message.text
        context.user_data['login'] = user_login

        if login.verification_user_from_login(context.user_data['id'], context.user_data['login']):
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_login_confirmed,
                parse_mode="MarkdownV2",
                reply_markup=markup,
            )
        else:
            markup = telegram.ReplyKeyboardMarkup(Buttons.loginBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].error_login_not_confirmed,
                parse_mode="MarkdownV2",
                reply_markup=markup,

            )

        return ConversationHandler.END

    @staticmethod
    async def cancel(update, context):
        markup = telegram.ReplyKeyboardMarkup(Buttons.loginBTN, resize_keyboard=True)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["answer"].answer_start,
            parse_mode="MarkdownV2",
            reply_markup=markup,
        )
        return ConversationHandler.END




    @staticmethod
    async def btn_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["answer"].answer_wait,
            reply_markup=markup
        )




    @staticmethod
    async def btn_visiting(update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = telegram.ReplyKeyboardMarkup(Buttons.visitingBTN, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["btn"].btn_visiting,
            reply_markup=markup
        )

    @staticmethod
    async def btn_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = telegram.ReplyKeyboardMarkup(Buttons.statusBTN, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["btn"].btn_stats,
            reply_markup=markup
        )

    @staticmethod
    async def btn_intheway(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        user_name = user.first_name
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

    @staticmethod
    async def btn_arrived(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        user_name = user.first_name
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        status = db.status.present(update.message.chat_id, user_name)
        print(status)
        if status is bool(True):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_info,
                reply_markup=markup
            )
        elif status == "Holiday":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_holiday,
                reply_markup=markup
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_status_updated,
                reply_markup=markup
            )

    @staticmethod
    async def btn_marks_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        user_name = user.first_name
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        thread_my_mark = threading.Thread(target=db.status.my_marks, args=[update.message.chat_id, user_name])
        thread_my_mark.start()
        status = thread_my_mark.join()
        if status is True:
            pass
        elif status is None:
            pass
            # await Bot.journal_registration()
        else:
            pass
            # await context.bot.send_message(
            #     chat_id=update.effective_chat.id,
            #     text=ui_text["answer"].answer_wait,
            #     reply_markup=markup
            # )

    class VisitingStatus:
        def __init__(self, absence, percent):
            week = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
            self.status = str("📅 *Відсутність по датам*:\n")
            iter_absence = iter(absence)
            for i in absence: # {week[datetime.datetime(i).weekday()]} -

                date = datetime.datetime.strptime(i, "%Y/%m/%d")
                self.status = self.status + f"       {week[date.weekday()]} \- ⌞{i}⌝\n"
                next(iter_absence)
            self.status = self.status + f"\n 🧮 *Відсоток Присутності \- _{str(percent).replace('.', ',')}%_*"

        def get_status(self):
            return self.status

    @staticmethod
    async def btn_visiting_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        user_name = user.first_name
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        result_queue = Queue()
        thread_visiting = threading.Thread(target=db.status.visiting, args=[update.message.chat_id, user_name, result_queue])
        thread_visiting.start()
        thread_visiting.join()

        result = result_queue.get()
        if result[0] is not None:
            visiting = Bot.VisitingStatus(result[0], result[1])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=visiting.get_status(),
                reply_markup=markup,
                parse_mode="MarkdownV2"
            )
        else:
            pass

        # if message == ui_text["btn"].btn_login:
        #     await context.bot.send_message(
        #         chat_id=update.effective_chat.id,
        #         text=ui_text["answer"].answer_login,
        #         parse_mode="MarkdownV2",
        #     )
        #
        #
        #
        #     await context.bot.send_message(
        #         chat_id=update.effective_chat.id,
        #         text=ui_text["answer"].answer_password,
        #         parse_mode="MarkdownV2",
        #     )

# TODO
#     @staticmethod
#     async def journal_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
#         await context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text=ui_text["answer"].answer_wait,
#         )


