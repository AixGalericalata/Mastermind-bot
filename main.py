from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from simple_bot import SimpleBot
from utils import to_byte_array
from image_utils import create_image
from io import BytesIO

TOKEN = '1714855501:AAHe0feLA42F36y-3luseYthox3gadVF5Rk'
num_colors = 8
num_symbols = 4


def reply_image(update, context):
    bot = context.user_data['bot']
    msg = to_byte_array(update.message.text, num_symbols, num_colors)
    if msg:
        answer = bot.get_answer(msg)
        context.user_data['moves'].append((msg, answer))
        image = create_image(context.user_data['moves'])
        bio = BytesIO()
        bio.name = 'image.png'
        image.save(bio, 'PNG')
        bio.seek(0)
        if answer[0] == num_symbols:
            context.bot.send_photo(
                update.message.chat_id,
                bio,
                caption=f'Поздравляю, вы угадали!'
            )
        else:
            context.bot.send_photo(
                update.message.chat_id,
                bio
            )
    else:
        update.message.reply_text(f'Ошибка.')


def reply_text(update, context):
    bot = context.user_data['bot']
    msg = to_byte_array(update.message.text, num_symbols, num_colors)
    if msg:
        answer = bot.get_answer(msg)
        if answer[0] == num_symbols:
            update.message.reply_text(f'Поздравляю, вы угадали!')
        else:
            update.message.reply_text(f'Быков: {answer[0]}, коров: {answer[1]}')
    else:
        update.message.reply_text(f'Ошибка.')


def start(update, context):
    bot = SimpleBot(num_colors, num_symbols)
    context.user_data['bot'] = bot
    context.user_data['moves'] = []
    update.message.reply_text(bot.get_greeting())


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, reply_image)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
