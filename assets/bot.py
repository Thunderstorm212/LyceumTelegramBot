import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from assets.ui import ui_text


class Buttons:
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
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].answer_home, reply_markup=markup)

    @staticmethod
    async def all_responses(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message.text

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
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_info,
                reply_markup=markup
            )

        if message == ui_text["btn"].btn_arrived:
            markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ui_text["answer"].answer_info,
                reply_markup=markup
            )


