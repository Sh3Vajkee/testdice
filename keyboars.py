from aiogram import types


def get_dice_keyboard():
    keyboard = [
        [
            types.KeyboardButton(text='🎲Сыграть'),
            types.KeyboardButton(text='🎯Сыграть')

        ],
        [
            types.KeyboardButton(text='🏀Сыграть'),
            types.KeyboardButton(text='⚽Сыграть'),
            types.KeyboardButton(text='🎳Сыграть')
        ]
    ]

    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
