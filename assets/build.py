import os
import sys
import telegram
import re
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
import conf
from lib import Colors, StatusBar
from assets.bot import Bot
import threading
from assets.ui import ui_text


def build():
    try:
        StatusBar(f"Bot {Colors(conf.BOT_ID, '#8ecae6')} starting", 3)

        app = Application.builder().token(conf.BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", Bot.star_command))
        # app.add_handler(CommandHandler("dev_mode", Bot.dev_mode))

        # app.add_handler(MessageHandler(filters.TEXT, Bot.all_responses))
        app.add_handler(MessageHandler(filters.CONTACT, Bot.registration_from_number))
        app.add_handler(
            ConversationHandler(
                entry_points=[
                    MessageHandler(filters.Regex(ui_text["btn"].btn_login), Bot.registration_start)
                ],
                states={
                    1: [MessageHandler(filters.TEXT, Bot.registration_login)],
                },
                fallbacks=[MessageHandler(filters.COMMAND, Bot.cancel)]
            ),
        )

        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_back), Bot.btn_back))
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_stats), Bot.btn_stats))
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_visiting), Bot.btn_visiting))
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_intheway), Bot.btn_intheway))
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_arrived), Bot.btn_arrived))
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_marks_status), Bot.btn_marks_status))
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_visiting_status), Bot.btn_visiting_status))

        # app.add_handler(ConversationHandler(
        #     entry_points=[
        #         MessageHandler(filters.MessageFilter(ui_text["btn"].btn_login), Bot.registration_start)
        #     ],
        #     states={
        #         LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, Bot.registration_login)],
        #         PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, Bot.registration_password)],
        #     }, fallbacks=[CommandHandler('cancel', Bot.cancel)]
        # )
        # )
        # states = {
        #              LOGIN: [MessageHandler(filters.MessageFilter() & ~filters.COMMAND, get_login)],
        #              PASSWORD: [MessageHandler(Filters.text & ~Filters.command, get_password)],
        #          },))


        # Run Bot
        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('work', '#588157')}.")
        app.run_polling(3)

    except Exception as e:
        print("file:")
        print(e, file=sys.stderr)
    finally:
        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('stop', '#d00000')}.")
        return

