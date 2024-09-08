import logging
import random
import redis
import re

from functools import partial
from enum import Enum
from environs import Env
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from collecting_content import get_content


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger('telegram_bot')


class States(Enum):
    CHOOSING = 1
    SCORE = 2


def start(update, _):
    user = update.message.from_user.first_name
    reply_keyboard = [
        ['Новый вопрос', 'Сдаться'],
        ['Мой счёт']
    ]
    markup_key = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    update.message.reply_text(
        f'Привет {user}! Я бот для викторины!\n\n'
        'Команда /cancel, чтобы прекратить разговор.\n\n',
        reply_markup=markup_key, )
    return States.CHOOSING


def handle_new_question_request(update, _, redis_db):
    user = update.message.from_user
    logger.info('%s: %s', user.first_name, update.message.text)
    quiz_content = get_content()
    question, answer = random.choice(list(quiz_content.items()))
    redis_db.set(user.id, answer)

    update.message.reply_text(
        text=question,
    )
    return States.SCORE


def handle_solution_attempt(update, _, redis_db):
    user = update.message.from_user
    logger.info('%s: %s', user.first_name, update.message.text)
    answer = re.sub(r"[\(\[].*?[\)\]]", "", redis_db.get(user.id)).strip()[:-1]
    if update.message.text == answer:
        reply_keyboard = [
            ['Новый вопрос'],
        ]
        markup_key = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )

        update.message.reply_text(
            text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
            reply_markup=markup_key,
        )
        return States.CHOOSING
    else:
        reply_keyboard = [
            ['Сдаться'],
        ]
        markup_key = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )

        update.message.reply_text(
            text='Неправильно… Попробуешь ещё раз?',
            reply_markup=markup_key,
        )
        return States.SCORE


def handle_give_up(update, _, redis_db):
    user = update.message.from_user
    logger.info('%s: %s', user.first_name, update.message.text)
    answer = re.sub(r"[\(\[].*?[\)\]]", "", redis_db.get(user.id)).strip()[:-1]
    reply_keyboard = [
        ['Новый вопрос'],
    ]
    markup_key = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    update.message.reply_text(
        text=answer,
        reply_markup=markup_key
    )
    return States.CHOOSING


def cancel(update, _):
    user = update.message.from_user
    logger.info('Пользователь %s отменил разговор.', user.first_name)
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться.\n'
        'До встречи!',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    env = Env()
    env.read_env()
    try:
        updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
        redis_server = redis.StrictRedis(
            host=env.str('REDIS_HOST'),
            port=env.int('REDIS_PORT'),
            password=env.str('REDIS_PASSWORD'),
            decode_responses=True,
            encoding='KOI8-R'
        )
        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],

            states={
                States.CHOOSING: [
                    MessageHandler(
                        Filters.regex('^Новый вопрос$'),
                        partial(handle_new_question_request, redis_db=redis_server),
                    )
                ],
                States.SCORE: [
                    MessageHandler(
                        Filters.regex('^Сдаться$'),
                        partial(handle_give_up, redis_db=redis_server),
                    ),
                    MessageHandler(
                        Filters.text,
                        partial(handle_solution_attempt, redis_db=redis_server),
                    )
                ],
            },

            fallbacks=[CommandHandler('cancel', cancel)],
        )

        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()
    except Exception as err:
        logging.error(err, exc_info=True)


if __name__ == '__main__':
    main()
