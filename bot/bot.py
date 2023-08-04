import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                'Список товаров', callback_data='last'
            ),
        ],
    ],
    resize_keyboard=True)


def start(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, я бот для парсинга товаров Ozon!',
        reply_markup=BUTTON
    )


def get_last(update, context):
    response = requests.get('http://localhost:8000/api/v1/products/')
    chat = update.effective_chat
    data = response.json()
    if not data:
        return context.bot.send_message(
            chat.id,
            text='Парсинг еще не запускался',
            reply_markup=BUTTON,
            parse_mode='html',
            disable_web_page_preview=True,
        )
    sending_data = [(item['title'], item['link']) for item in data]
    message = 'Список товаров:\n\n'

    for index, (title, link) in enumerate(sending_data, start=1):
        message += (f'{index}. {title}: '
                    f'<a href="{link}">Посмотреть</a>\n')

        if not index % 10:
            context.bot.send_message(
                chat.id,
                text=message,
                reply_markup=BUTTON,
                parse_mode='html',
                disable_web_page_preview=True,
            )
            message = ''

    if message:
        context.bot.send_message(
            chat.id,
            text=message,
            reply_markup=BUTTON,
            parse_mode='html',
            disable_web_page_preview=True,
        )
