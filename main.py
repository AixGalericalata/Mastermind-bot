from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from simple_bot import SimpleBot
from utils import to_byte_array
from image_utils import create_image
from io import BytesIO
from lib import cip_keyboard, reply_keyboard, return_keyboard, storage, start_keyboard
from caesars import caesars_cipher
from enigma import enigma_code
from code import from_cipher, to_cipher

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
com_return = ReplyKeyboardMarkup(return_keyboard, one_time_keyboard=False)
cip = ReplyKeyboardMarkup(cip_keyboard, one_time_keyboard=False)
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)

TOKEN = '1751999231:AAEDSJALf8fgXIySv0wfDVYg6aE-LLJgYHg'
levels_keyboard = [['Классический', 'Обычный', 'Продвинутый'],
                   ['Правила', '/stop']]
stop_keyboard = [['/stop']]


def reply(update, context):
    message = update.message.text
    if message == '/stop':
        update.message.reply_text('OK', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    bot = context.user_data.get('bot')
    if bot:
        reply_image(update, context)
        return 1
    if message == 'Правила':
        update.message.reply_text(
            'https://ru.wikipedia.org/wiki/%D0%91%D1%8B%D0%BA%D0%B8_%D0%B8_%D0%BA%D0%BE%D1%80%D0%BE%D0%B2%D1%8B',
            reply_markup=ReplyKeyboardMarkup(levels_keyboard,
                                             one_time_keyboard=True))
        return 1
    if message == 'Классический':
        bot = SimpleBot(9, 4, False)
    elif message == 'Обычный':
        bot = SimpleBot(6, 4, True)
    elif message == 'Продвинутый':
        bot = SimpleBot(8, 5, True)
    else:
        update.message.reply_text('Если хотите закончить игру, напишите /stop.',
                                  reply_markup=ReplyKeyboardMarkup(stop_keyboard,
                                                                   one_time_keyboard=False))
        return 1
    context.user_data['bot'] = bot
    context.user_data['moves'] = []
    update.message.reply_text(bot.get_greeting(), reply_markup=ReplyKeyboardMarkup(stop_keyboard,
                                                                                   one_time_keyboard=False))


def reply_image(update, context):
    bot = context.user_data['bot']
    msg = to_byte_array(update.message.text, bot.num_symbols, bot.num_colors, bot.repetition)
    if msg == '/stop':
        update.message.reply_text('Вы уверены? Если да, то напишите /stop.')
        return 1
    if type(msg) == str:
        update.message.reply_text(msg)
        return 1
    answer = bot.get_answer(msg)
    context.user_data['moves'].append((msg, answer))
    image = create_image(context.user_data['moves'])
    bio = BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    if answer[0] == bot.num_symbols:
        context.bot.send_photo(
            update.message.chat_id,
            bio,
            caption=f'Поздравляю, вы угадали! Игра окончена.'
        )
        context.user_data.clear()
    else:
        context.bot.send_photo(
            update.message.chat_id,
            bio
        )


def start_mastermind(update, context: CallbackContext):
    storage['game'] = 1
    context.user_data.clear()
    update.message.reply_text('Выберите режим игры:',
                              reply_markup=ReplyKeyboardMarkup(levels_keyboard,
                                                               one_time_keyboard=True))
    return 1


def start_cipher(update, context):
    update.message.reply_text(
        "Выбирите тип шифра:", reply_markup=markup)
    return 1


def start(update, context: CallbackContext):
    storage['game'] = 0
    context.user_data.clear()
    update.message.reply_text("Ты можешь поиграть MasterMind\n"
                              "Или ты можешь зашифровать текст,\n"
                              "Что делать будем?", reply_markup=start_markup)
    return ConversationHandler.END


def close_keyboard(update, context):
    update.message.reply_text('OK', reply_markup=ReplyKeyboardRemove())


def stop(update, context):
    return ConversationHandler.END


def first_response(update, context):
    text = update.message.text
    if text == 'Enigma':
        storage['cipher'] = text
        update.message.reply_text(
            "Что делать будем?", reply_markup=cip)
    elif text == 'Шифр Цезаря':
        storage['cipher'] = text
        update.message.reply_text(
            "Что делать будем?", reply_markup=cip)
    elif text == 'Двоичный код':
        storage['cipher'] = text
        update.message.reply_text(
            "Что делать будем?", reply_markup=cip)
    elif text == 'return':
        close_keyboard(update, context)
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "Чего не умею, того не умею.")
    return 4


def second_response(update, context):
    text = update.message.text
    if text == 'return':
        update.message.reply_text('OK', reply_markup=markup)
        return 1
    elif text.lower() == 'Зашифровать'.lower():
        if storage['cipher'].lower() == 'Enigma'.lower():
            update.message.reply_text(
                "Для начала нужно ввести 3 ключя для роторов,\n"
                " а затем через '-' ввести текст на англиском,\n"
                " состояший только из букв и пробелов.\n"
                " Пример: ABC-Hello World.",
                reply_markup=com_return)
            return 5
        elif storage['cipher'].lower() == 'Двоичный код'.lower():
            answer = """Ввод: <текст>"""
            update.message.reply_text(answer, reply_markup=com_return)
        elif storage['cipher'].lower() == 'Шифр Цезаря'.lower():
            answer = "Ввод: <ключ>-<текст>\n" \
                     "Ключ-Одно число от 1 до 26."
            update.message.reply_text(answer, reply_markup=com_return)
        elif storage['cipher'].lower() == 'Азбука Морзе'.lower():
            answer = """Ввод: <текст>"""
            update.message.reply_text(answer, reply_markup=com_return)
        return 2
    elif text.lower() == 'Расшифровать'.lower():
        if storage['cipher'].lower() == 'Enigma'.lower():
            update.message.reply_text(
                "Для начала нужно ввести 3 ключи для роторов,\n"
                "которые были использованный для шифровки,"
                "затем через '-' ввести шифр на англиском,\n"
                "состояший только из букв и пробелов.\n"
                "Пример: ABC-FPXKE HWZEQ.",
                reply_markup=com_return)
            return 5
        elif storage['cipher'].lower() == 'Двоичный код'.lower():
            answer = """Ввод: <код>"""
            update.message.reply_text(answer, reply_markup=com_return)
        elif storage['cipher'].lower() == 'Шифр Цезаря'.lower():
            answer = "Ввод: <ключ>-<шифр>\n" \
                     "Ключ-Число, которое использовалось для шифровки."
            update.message.reply_text(answer, reply_markup=com_return)
        elif storage['cipher'].lower() == 'Азбука Морзе'.lower():
            answer = """Ввод: <шифр>"""
            update.message.reply_text(answer, reply_markup=com_return)
        return 3
    return 4


def enigma_response(update, context):
    text = update.message.text
    if text == 'return':
        update.message.reply_text('OK', reply_markup=markup)
        return 1
    else:
        try:
            enigma = enigma_code(text)
        except Exception:
            update.message.reply_text('Вы вели слишком много ключей\n'
                                      'или ошиблись в типе данных, ввели посторонние символы!')
            return 5
        update.message.reply_text(f"Вот что получилось: {''.join(enigma)}")
    return 5


def encrypt_response(update, context):
    text = update.message.text
    if text == 'return':
        update.message.reply_text('OK', reply_markup=markup)
        return 1
    if storage['cipher'].lower() == 'Двоичный код'.lower():
        cipher_text = to_cipher(text)
    elif storage['cipher'].lower() == 'Шифр Цезаря'.lower():
        try:
            key, text = text.split('-')[0], text.split('-')[1]
            if int(key) > 26 or int(key) < 1:
                update.message.reply_text('Неправильный ключ')
                return 2
            cipher_text = caesars_cipher(int(key), text)
            if len(cipher_text) == 0:
                update.message.reply_text('Ошибка в типе введенных данных.')
                return 2
        except Exception:
            update.message.reply_text('Вы вели слишком много ключей\n'
                                      'или ошиблись в типе данных, ввели посторонние символы!')
    update.message.reply_text(
        f"Вот что получилось: {cipher_text}")
    return 2


def decrypt_response(update, context):
    text = update.message.text
    if text == 'return':
        update.message.reply_text('OK', reply_markup=markup)
        return 1
    if storage['cipher'].lower() == 'Двоичный код'.lower():
        try:
            cipher_text = from_cipher(text)
        except Exception:
            update.message.reply_text('Вы точно ввели код')
    elif storage['cipher'].lower() == 'Шифр Цезаря'.lower():
        try:
            key, text = text.split('-')[0], text.split('-')[1]
            if int(key) > 26 or int(key) < 1:
                update.message.reply_text('Неправильный ключ')
                return 2
            cipher_text = caesars_cipher(int(key) * -1, text)
        except Exception:
            update.message.reply_text('Вы вели слишком много ключей\n'
                                      'или ошиблись в типе данных, ввели посторонние символы!')
    update.message.reply_text(
        f"Вот что получилось: {cipher_text}")
    return 3


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


cipher = ConversationHandler(
    entry_points=[CommandHandler('cipher', start_cipher)],
    states={
        1: [MessageHandler(Filters.text, first_response)],
        2: [MessageHandler(Filters.text, encrypt_response)],
        3: [MessageHandler(Filters.text, decrypt_response)],
        4: [MessageHandler(Filters.text, second_response)],
        5: [MessageHandler(Filters.text, enigma_response)],
    },
    fallbacks=[CommandHandler('stop', stop)])

master = ConversationHandler(
    entry_points=[CommandHandler('mastermind', start_mastermind)],
    states={
        1: [MessageHandler(Filters.text, reply)]
    },
    fallbacks=[CommandHandler('stop', stop)])


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(master)
    dp.add_handler(cipher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
