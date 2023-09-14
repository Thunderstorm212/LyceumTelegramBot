from lib import Colors, StatusBar
from assets.bot import Bot
from assets.admin import Admin
import conf
import os
import sys
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from ui import ui_text


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


async def star_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["answer"].answer_home, reply_markup=markup)


async def all_responses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    if message == ui_text["btn"].btn_back:
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["btn"].btn_home, reply_markup=markup)

    if message == ui_text["btn"].btn_visiting:
        markup = telegram.ReplyKeyboardMarkup(Buttons.visitingBTN, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ui_text["btn"].btn_visiting, reply_markup=markup)

    if message == ui_text["btn"].btn_intheway:
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Дякую за інформацію ", reply_markup=markup)

    if message == ui_text["btn"].btn_arrived:
        markup = telegram.ReplyKeyboardMarkup(Buttons.homeBTN, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Дякую за інформацію ", reply_markup=markup)


if __name__ == '__main__':
    try:
        StatusBar(f"Bot {Colors(conf.BOT_ID, '#8ecae6')} starting", 3)
        app = Application.builder().token(conf.BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", star_command))
        app.add_handler(MessageHandler(filters.TEXT, all_responses))

        # Run Bot
        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('work', '#588157')}.")
        app.run_polling(poll_interval=3)

        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('stop', '#d00000')}.")
    except Exception as e:
        print("file:")
        print(e, file=sys.stderr)
