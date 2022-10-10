from aiogram import Router, types
from aiogram.filters.text import Text
from globals import TEXT_ANSWER, mongo_db, bot
from components.keyboards import get_keyboard_cost

router = Router()


@router.message(Text(text=[TEXT_ANSWER['ENG']['task_btn_txt'], TEXT_ANSWER['RUS']['task_btn_txt']]))
async def with_puree(message: types.Message):
    user = await mongo_db.find_user(message.chat.id)
    await message.answer(
        TEXT_ANSWER[user['language']]['selection_cost'],
        reply_markup=await get_keyboard_cost()
    )


@router.callback_query(Text(startswith="new_cost_"))
async def callbacks_num(callback: types.CallbackQuery):
    cost = int(callback.data.split("_")[2])
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    user = await mongo_db.find_user(chat_id)

    new_task_status = await mongo_db.add_task_cost(chat_id, cost, message_id, user['language'])
    await callback.message.delete_reply_markup()
    if new_task_status:
        await bot.send_message(
            chat_id,
            TEXT_ANSWER[user['language']]['add_task_cost'].format(cost),
            reply_to_message_id=message_id)
    else:
        await bot.send_message(
            chat_id,
            TEXT_ANSWER[user['language']]['update_task_cost'].format(cost),
            reply_to_message_id=message_id)
    await callback.answer()
