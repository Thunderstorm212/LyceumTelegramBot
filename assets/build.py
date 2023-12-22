import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import conf
from utils import Colors, StatusBar
from assets.bot import Bot
from assets.ui import ui_text


def build():
    try:
        StatusBar(f"Bot {Colors(conf.BOT_ID, '#8ecae6')} starting", 3)
        app = Application.builder().token(conf.BOT_TOKEN).build()

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
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_group_leader), Bot.btn_group_leader))
        app.add_handler(ConversationHandler(
                entry_points=[
                    MessageHandler(filters.Regex(ui_text["btn"].btn_advertisement), Bot.btn_advertisement)
                ],
                states={
                    1: [MessageHandler(filters.TEXT, Bot.btn_advertisement_message)],
                },
                fallbacks=[MessageHandler(filters.COMMAND, Bot.cancel)]
            ),)
        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_homework), Bot.btn_homework))

        app.add_handler(MessageHandler(filters.Regex(ui_text["btn"].btn_menu), Bot.btn_menu))

        app.add_handler(
            ConversationHandler(
                entry_points=[
                    MessageHandler(filters.Regex(ui_text["btn"].btn_journal_account), Bot.btn_journal_start)
                ],
                states={
                    1: [MessageHandler(filters.TEXT, Bot.journal_login)],
                    2: [MessageHandler(filters.TEXT, Bot.journal_password)],
                },
                fallbacks=[MessageHandler(filters.TEXT & (~ filters.COMMAND), Bot.cancel)]
            ),
        )

        app.add_handler(CommandHandler("start", Bot.start_command))

        # Run Bot
        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('work', '#588157')}.")
        app.run_polling(3)

    except Exception as e:
        print("file:")
        print(e, file=sys.stderr)
    finally:
        print(f"\nBot {Colors(conf.BOT_ID, '#8ecae6')} {Colors('stop', '#d00000')}.")
        exit()
