from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

enter_num = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Текстом'),
            KeyboardButton(text='По фото')
        ],
        [
            KeyboardButton(text='Помощь')
        ]
    ],
    resize_keyboard=True
)