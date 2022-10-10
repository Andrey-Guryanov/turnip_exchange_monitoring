from aiogram import Router, types
from aiogram.filters.text import Text
from aiogram.filters.command import Command
from aiogram.types import Message
from globals import TEXT_ANSWER, mongo_db
from components.keyboards import get_keyboard_start, get_keyboard_actions

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        TEXT_ANSWER['START']['TEXT'],
        reply_markup=await get_keyboard_start(
            rus_btn_txt=TEXT_ANSWER['START']['RUS_BTN'],
            rus_callback='start_rus',
            eng_btn_txt=TEXT_ANSWER['START']['ENG_BTN'],
            eng_callback='start_eng',
        )
    )


@router.callback_query(Text(startswith="start_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    chat_id = callback.message.chat.id
    user = await mongo_db.find_user(chat_id)

    if user is None:
        await mongo_db.create_user(chat_id, callback.message.chat.username, action.upper())
    elif user is not None and user['language'] != action:
        await mongo_db.update_language_user(user['_id'], action.upper())

    if action == "rus":
        await callback.message.answer(
            TEXT_ANSWER['RUS']['title_text'],
            reply_markup=await get_keyboard_actions(
                get_btn_txt=TEXT_ANSWER['RUS']['get_btn'],
                task_btn_txt=TEXT_ANSWER['RUS']['task_btn_txt'],
            )
        )

    elif action == "eng":
        await callback.message.answer(
            TEXT_ANSWER['ENG']['title_text'],
            reply_markup=await get_keyboard_actions(
                get_btn_txt=TEXT_ANSWER['ENG']['get_btn'],
                task_btn_txt=TEXT_ANSWER['ENG']['task_btn_txt'],
            )
        )
    await callback.answer()
