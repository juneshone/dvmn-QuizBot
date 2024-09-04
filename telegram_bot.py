import logging

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


logger = logging.getLogger('telegram_bot')


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.full_name
    button_list = [
        [
            InlineKeyboardButton("Новый вопрос", callback_data='1'),
            InlineKeyboardButton("Сдаться", callback_data='2'),
        ],
        [InlineKeyboardButton("Мой счёт", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    update.message.reply_text(
        f'Привет {user}! Я бот для викторины!',
        reply_markup=reply_markup,
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    env = Env()
    env.read_env()

    logger.info('Бот запущен')

    updater = Updater(token=env.str('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
