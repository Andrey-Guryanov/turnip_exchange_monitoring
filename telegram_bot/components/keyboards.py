from aiogram import types


async def get_keyboard_start(rus_btn_txt: str,
                             rus_callback: str,
                             eng_btn_txt: str,
                             eng_callback: str):
    buttons = [
        [
            types.InlineKeyboardButton(text=eng_btn_txt, callback_data=eng_callback),
            types.InlineKeyboardButton(text=rus_btn_txt, callback_data=rus_callback),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_cost():
    buttons = [
        [
            types.InlineKeyboardButton(text='500💰', callback_data='new_cost_500'),
            types.InlineKeyboardButton(text='400💰', callback_data='new_cost_400'),
        ],
        [
            types.InlineKeyboardButton(text='300💰', callback_data='new_cost_300'),
            types.InlineKeyboardButton(text='200💰', callback_data='new_cost_200'),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_actions(get_btn_txt: str, task_btn_txt: str):
    buttons = [
        [
            types.KeyboardButton(text=get_btn_txt),
        ],
        [
            types.KeyboardButton(text=task_btn_txt),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
