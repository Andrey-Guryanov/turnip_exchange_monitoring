from asyncio import sleep
from globals import bot
from aiogram.exceptions import TelegramNetworkError


async def send_user_message(
        chat_id,
        text_message,
        parse_mode=None,
        reply_to_message_id=None):
    try:
        await bot.send_message(
            chat_id,
            text_message,
            parse_mode=parse_mode,
            reply_to_message_id=reply_to_message_id)
    except TelegramNetworkError:
        print('TelegramNetworkError')
        await sleep(1)
        await send_user_message(chat_id, text_message, parse_mode, reply_to_message_id)
