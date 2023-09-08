import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler


class Bot:
    def __init__(self):
        super(Bot, self).__init__()


async def star_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is start message")
