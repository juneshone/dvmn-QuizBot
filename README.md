# dvmn-QuizBot

Чат-бот для тестирования соискателей на стажировку.

## Подготовка к запуску проекта

1. Python должен быть уже установлен. Склонируйте репозиторий и создайте виртуальную среду командой:

```python
python -m venv venv
```

2. Активируйте виртуальную среду для Windows:

```python
.\venv\Scripts\activate.bat
```
для Linux:

```python
source venv/bin/activate
```

3. Затем используйте pip для установки зависимостей:

```python
pip install -r requirements.txt
```

4. Зарегистрируйте бота в Telegram и получите его токен. Чтобы сгенерировать токен, вам нужно поговорить с `@BotFather` и выполнить несколько простых шагов описанных [здесь](https://core.telegram.org/bots#6-botfather).
5. Создайте сообщество VK и получите его токен.
6. Заведите базу данных [Redis](https://redis.io/). Вы получите адрес базы данных вида: `redis-13965.f18.us-east-4-wc1.cloud.redislabs.com`, его порт вида: 16635 и его пароль.

## Переменнные окружения

Часть данных проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и присвойте значения переменным окружения в формате: ПЕРЕМЕННАЯ=значение.

_Переменные окружения проекта:_

```ini
TELEGRAM_BOT_TOKEN — токен доступа к Telegram-боту.
REDIS_HOST — хост или IP-адрес БД.
REDIS_PORT — номер порта БД.
REDIS_PASSWORD — пароль БД.
VK_GROUP_TOKEN — идентификатор сообщества VK. Токен VK можно получить в настройках сообщества.
```

## Как запустить

Убедитесь, что в терминале находитесь в директории кода и запустите бота, используя команды:

```python
python .\telegram_bot.py
```
или

```python
python .\vk_bot.py
```
_Примеры работы ботов:_

![vk_bot](https://github.com/juneshone/dvmn-QuizBot/blob/main/examination_vk.gif)

Ссылка на vk-бота [здесь](https://vk.com/club226476141).

![tg_bot](https://github.com/juneshone/dvmn-QuizBot/blob/main/examination_tg.gif)

Ссылка на telegram-бота [здесь](https://t.me/VerbGame_support_bot).

## Цель проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
