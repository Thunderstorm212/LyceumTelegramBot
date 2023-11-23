import datetime
import telegram
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from assets.ui import ui_text
from db import login
import db
import threading
from queue import Queue
from assets.chats_data import ChatData


class Buttons:
    loginBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_number, request_contact=True),
            telegram.KeyboardButton(ui_text["btn"].btn_login),

        ]
    ]
    homeBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_journal_account),
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

    menuBTN = [
        [
            telegram.KeyboardButton(ui_text["btn"].btn_news),
            telegram.KeyboardButton(ui_text["btn"].btn_group_leader),
        ],
        [
            telegram.KeyboardButton(ui_text["btn"].btn_settings),
            telegram.KeyboardButton(ui_text["btn"].btn_back),
        ]
    ]


class Bot(Buttons):

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
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

        if login.verification_user_with_id(update.effective_chat.id):
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
            chat_data_query = {
                str(update.effective_chat.id): {
                    "info": {}
                }
            }
            if ChatData().get_by_id(str(update.effective_chat.id)) is None:
                ChatData().add_obj(chat_data_query)

    @staticmethod
    async def registration_from_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
        contact = update.message.contact
        contact_phone_number = contact.phone_number.replace("+", "")
        if login.verification_user(update.effective_chat.id, contact_phone_number):
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=ui_text["answer"].answer_login_confirmed, reply_markup=markup, parse_mode="MarkdownV2")
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

        if login.verification_user_from_login(context.effective_chat.id, context.user_data['login']):
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
    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = telegram.ReplyKeyboardMarkup(Buttons.loginBTN, resize_keyboard=True)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["answer"].answer_canceled,
            parse_mode="MarkdownV2",
            reply_markup=markup,
        )
        return ConversationHandler.END

    @staticmethod
    async def btn_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["answer"].answer_develop,
        )

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

        if db.status.in_the_way(update.effective_chat.id, user_name):
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
        status = db.status.present(update.effective_chat.id, user_name)
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
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)

        result_queue_journal = Queue()
        thread_journal = threading.Thread(target=login.verification_user_journal,
                                          args=[update.effective_chat.id, result_queue_journal])
        thread_journal.start()
        thread_journal.join()
        journal_user = result_queue_journal.get()

        if journal_user[0] is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_journal_not_registered,
                parse_mode="MarkdownV2",
                reply_markup=markup
            )

        elif type(journal_user[0]) is str:
            context.user_data['journal_login'] = journal_user[0]
            context.user_data['journal_password'] = journal_user[1]

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_wait,
                reply_markup=markup
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["error"].error_unknown,
            )

        result_queue = Queue()
        thread_my_mark = threading.Thread(target=db.status.my_marks, args=[
            update.effective_chat.id,
            result_queue
        ])
        thread_my_mark.start()
        thread_my_mark.join()
        result = result_queue.get()
        if type(result) is str:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=result,
                reply_markup=markup,
                parse_mode="MarkdownV2",
            )
        elif result is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_markup=markup,
                text=ui_text["answer"].answer_update
            )
            result_queue = Queue()
            thread_journal = threading.Thread(target=login.login_in_journal,
                                              args=[
                                                  update.effective_chat.id,
                                                  context.user_data['journal_login'],
                                                  context.user_data['journal_password'],
                                                  result_queue
                                              ])
            thread_journal.start()
            thread_journal.join()
            journal_result = result_queue.get()

            if journal_result:
                result_queue = Queue()
                thread_my_mark = threading.Thread(target=db.status.my_marks, args=[
                    update.effective_chat.id,
                    result_queue
                ])
                thread_my_mark.start()
                thread_my_mark.join()
                result = result_queue.get()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=result,
                    reply_markup=markup,
                    parse_mode="MarkdownV2"
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=ui_text["error"].error_unknown,
                    reply_markup=markup,
                    parse_mode="MarkdownV2",

                )

        else:
            pass

    class VisitingStatus:
        def __init__(self, absence, percent):
            week = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
            self.status = str("📅 *Відсутність по датам*:\n")
            iter_absence = iter(absence)
            for i in absence:

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
        thread_visiting = threading.Thread(target=db.status.visiting, args=[update.effective_chat.id, user_name, result_queue])
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
        elif int(result[1]) == 100:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_visiting_no_gaps,
                reply_markup=markup,
                parse_mode="MarkdownV2"
            )

        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].error_unknown,
                reply_markup=markup,
                parse_mode="MarkdownV2"
            )

    @staticmethod
    async def btn_journal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        result_queue = Queue()
        thread_journal = threading.Thread(target=login.verification_user_journal, args=[update.effective_chat.id, result_queue])
        thread_journal.start()
        thread_journal.join()

        journal_user = result_queue.get()

        if journal_user[0] is None:
            markup_remove = telegram.ReplyKeyboardRemove()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_journal_not_registered,
                parse_mode="MarkdownV2",
                reply_markup=markup_remove
            )

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_journal_login,
                parse_mode="MarkdownV2"
            )
            return 1
        elif type(journal_user[0]) is str:
            context.user_data['journal_login'] = journal_user[0]
            context.user_data['journal_password'] = journal_user[1]

            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_wait,
                reply_markup=markup
            )
            return ConversationHandler.END
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["error"].error_unknown,
            )
            return ConversationHandler.END

    @staticmethod
    async def journal_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
        journal_login = update.message.text
        context.user_data['journal_login'] = journal_login
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["answer"].answer_journal_password,
            parse_mode="MarkdownV2"
        )
        return 2

    @staticmethod
    async def journal_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)

        journal_password = update.message.text
        context.user_data['journal_password'] = journal_password
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ui_text["answer"].answer_wait_parse,
            parse_mode="MarkdownV2"
        )
        result_queue = Queue()
        thread_journal = threading.Thread(target=login.login_in_journal,
                                          args=[
                                              update.effective_chat.id,
                                              context.user_data['journal_login'],
                                              context.user_data['journal_password'],
                                              result_queue
                                          ])
        thread_journal.start()
        thread_journal.join()
        journal_result = result_queue.get()
        if journal_result:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_journal_registration_ok,
                reply_markup=markup,
                parse_mode="MarkdownV2"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["error"].error_journal_registration,
                reply_markup=markup,
                parse_mode="MarkdownV2",

            )
        return ConversationHandler.END
