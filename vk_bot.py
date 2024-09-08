import logging

import vk_api as vk
from environs import Env
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


logger = logging.getLogger('vk_bot')


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)

    try:
        logger.info('VK Бот запущен')
        vk_session = vk.VkApi(token=env.str('VK_GROUP_TOKEN'))
        vk_api = vk_session.get_api()

        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Белая кнопка', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()  # Переход на вторую строку
        keyboard.add_button('Красная кнопка', color=VkKeyboardColor.NEGATIVE)

        keyboard.add_line()
        keyboard.add_button('Синяя кнопка', color=VkKeyboardColor.PRIMARY)

        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                vk_api.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message='Пример клавиатуры'
                )
    except Exception as err:
        logger.error(err, exc_info=True)

        
if __name__ == "__main__":
    main()
