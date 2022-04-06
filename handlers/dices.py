from asyncio import sleep
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from keyboars import get_dice_keyboard


async def cmd_start(message: types.Message):
    await message.answer('Выберите мини-игру', reply_markup=get_dice_keyboard())


async def cmd_stop(message: types.Message):
    await message.answer('Клавиатура удалена.\nЧтобы вернуть клавиатуру нажмите\n/start', reply_markup=types.ReplyKeyboardRemove())


async def cmd_dice(message: types.Message):
    msg = await message.answer_dice()
    await sleep(3)
    await message.answer(f'Вам выпало число - <b>{msg.dice.value}</b>!')


async def cmd_darts(message: types.Message):
    msg = await message.answer_dice('🎯')
    await sleep(3)

    result = msg.dice.value
    if result == 1:
        await message.answer('Неудачно! Вы промазали.')
    elif result == 6:
        await message.answer(f'В яблочко! Вы заработали {result} очков.')
    elif result == 5:
        await message.answer(f'Вы заработали {result} очков.')
    else:
        await message.answer(f'Вы заработали {result} очка.')


async def cmd_basket(message: types.Message):
    msg = await message.answer_dice('🏀')
    await sleep(4)

    result = msg.dice.value
    if result in [1, 2, 3]:
        await message.answer('Промах!')
    else:
        await message.answer('Удачное попадание!')


async def cmd_football(message: types.Message):
    msg = await message.answer_dice('⚽')
    await sleep(4)

    result = msg.dice.value
    if result == 1:
        await message.answer('Промах! Выше ворот.')
    elif result == 2:
        await message.answer('Штанга!')
    elif result == 5:
        await message.answer('Гол! Ровно в девяточку!')
    else:
        await message.answer('Гол!')


async def cmd_bowling(message: types.Message):
    msg = await message.answer_dice('🎳')
    await sleep(3)

    result = msg.dice.value
    if result == 1:
        await message.answer('Промах! Вы выбили 0 очков.')
    elif result == 6:
        await message.answer('Страйк! Вы выбили 6 очков.')
    elif result == 2:
        await message.answer('Вы выбили 1 очко.')
    else:
        await message.answer(f'Вы выбили {result} очка.')


def dices_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_stop, commands='stop')
    dp.register_message_handler(cmd_dice, Text(equals='🎲Сыграть'))
    dp.register_message_handler(cmd_darts, Text(equals='🎯Сыграть'))
    dp.register_message_handler(cmd_basket, Text(equals='🏀Сыграть'))
    dp.register_message_handler(cmd_football, Text(equals='⚽Сыграть'))
    dp.register_message_handler(cmd_bowling, Text(equals='🎳Сыграть'))
