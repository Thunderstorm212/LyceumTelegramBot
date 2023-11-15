import os
import sys
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import conf
from lib import Colors, StatusBar
from assets.bot import Bot
import threading


def build():
    try:
        StatusBar(f"Bot {Colors(conf.BOT_ID, '#8ecae6')} starting", 3)

        app = Application.builder().token(conf.BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", Bot.star_command))
        app.add_handler(CommandHandler("dev_mode", Bot.dev_mode))

        app.add_handler(MessageHandler(filters.TEXT, Bot.all_responses))
        app.add_handler(MessageHandler(filters.CONTACT, Bot.registration))

        # Run Bot
        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('work', '#588157')}.")
        app.run_polling(3)

    except Exception as e:
        print("file:")
        print(e, file=sys.stderr)
    finally:
        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('stop', '#d00000')}.")
        return

