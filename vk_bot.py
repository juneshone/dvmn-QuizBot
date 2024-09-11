import logging
import random
import redis
import re

import vk_api as vk
from environs import Env
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from collecting_content import get_content


logger = logging.getLogger('vk_bot')


def handle_new_question_request(event, vk_api, redis_db, keyboard, content_folder):
    user = event.user_id
    username = vk_api.users.get(user_ids=user)[0]['first_name']
    logger.info('%s(%s): %s', username, user, event.text)
    quiz_content = get_content(content_folder)
    question, answer = random.choice(list(quiz_content.items()))
    redis_db.set(user, answer)

    vk_api.messages.send(
        peer_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=question
    )


def handle_solution_attempt(event, vk_api, redis_db, keyboard):
    user = event.user_id
    username = vk_api.users.get(user_ids=user)[0]['first_name']
    logger.info('%s(%s): %s', username, user, event.text)
    answer = re.sub(r"[\(\[].*?[\)\]]", "", redis_db.get(user)).strip()[:-1]
    if event.text == answer:

        vk_api.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
        )
    else:

        vk_api.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Неправильно… Попробуешь ещё раз?'
        )


def handle_give_up(event, vk_api, redis_db, keyboard):
    user = event.user_id
    username = vk_api.users.get(user_ids=user)[0]['first_name']
    logger.info('%s(%s): %s', username, user, event.text)
    answer = re.sub(r"[\(\[].*?[\)\]]", "", redis_db.get(user)).strip()[:-1]

    vk_api.messages.send(
        peer_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=f'Вот тебе правильный ответ:\n'
                f'{answer}\n\n'
                f' Чтобы продолжить, нажми «Новый вопрос»'
    )


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)

    try:
        logger.info('VK-бот запущен')
        content_folder = env.str('CONTENT_FOLDER')
        vk_session = vk.VkApi(token=env.str('VK_GROUP_TOKEN'))
        vk_api = vk_session.get_api()
        redis_server = redis.StrictRedis(
            host=env.str('REDIS_HOST'),
            port=env.int('REDIS_PORT'),
            password=env.str('REDIS_PASSWORD'),
            decode_responses=True,
            encoding='KOI8-R'
        )

        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Сдаться', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Счёт', color=VkKeyboardColor.NEGATIVE)

        keyboard.add_line()
        keyboard.add_button('Завершить', color=VkKeyboardColor.NEGATIVE)

        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Привет':
                    vk_api.messages.send(
                        peer_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='Приветствую тебя в нашей викторине!\n'
                                'Чтобы продолжить, нажми «Новый вопрос»'
                                'Чтобы прекратить разговор, нажми «Завершить диалог»'
                    )
                    continue
                if event.text == 'Новый вопрос':
                    handle_new_question_request(
                        event, vk_api, redis_server, keyboard, content_folder
                    )
                    continue
                if event.text == 'Сдаться':
                    handle_give_up(event, vk_api, redis_server, keyboard)
                    continue
                if event.text == 'Завершить':
                    vk_api.messages.send(
                        peer_id=event.user_id,
                        random_id=get_random_id(),
                        message='Мое дело предложить - Ваше отказаться.\n'
                                'До встречи!'
                    )
                    continue
                handle_solution_attempt(event, vk_api, redis_server, keyboard)
    except Exception as err:
        logger.error(err, exc_info=True)


if __name__ == "__main__":
    main()
