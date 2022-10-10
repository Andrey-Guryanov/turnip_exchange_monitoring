from aiogram import Router, types
from aiogram.filters.text import Text
from globals import TEXT_ANSWER, mongo_db

router = Router()


@router.message(Text(text=[TEXT_ANSWER['ENG']['get_btn'], TEXT_ANSWER['RUS']['get_btn']]))
async def with_puree(message: types.Message):
    user = await mongo_db.find_user(message.chat.id)
    new_task_status = await mongo_db.add_task_no_cost(message.chat.id, 0, message.message_id, user['language'])
    if new_task_status:
        await message.reply(TEXT_ANSWER[user['language']]['add_task_no_cost'])
    else:
        await message.reply(TEXT_ANSWER[user['language']]['wait_task_no_cost'])