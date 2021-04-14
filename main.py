from telegram.ext import Updater, MessageHandler, Filters

TOKEN = '1714855501:AAHe0feLA42F36y-3luseYthox3gadVF5Rk'


def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
