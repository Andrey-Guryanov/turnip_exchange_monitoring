from globals import mongo_db, TEXT_ANSWER
from aiogram import html


async def _create_islands_text(islands: list, language: str) -> str:
    islands_text = ''
    title = TEXT_ANSWER[language]['title_task_no_cost']
    for island in islands:
        island_name = island['name']
        island_dsc = island['description'].replace('\n\n', '\n').strip()
        turnip_cost = island['turnip_cost']
        island_url = island['url']
        island_queue = [
            island['queue']['count_waiting'],
            island['queue']['length'], ]
        islands_text += TEXT_ANSWER[language]['completed_task_no_cost'].format(
            html.quote(island_name),
            html.quote(island_dsc),
            turnip_cost,
            island_queue[0],
            island_queue[1],
            island_url, ) + '🌴' * 5
    return title + islands_text


async def send_messages_task(bot) -> None:
    while True:
        task = await mongo_db.check_completed_task()
        if task is None:
            break
        else:
            island_name = task['result']['islands'][0]['name']
            island_dsc = task['result']['islands'][0]['description'].replace('\n\n', '\n').strip()
            turnip_cost = task['result']['islands'][0]['turnip_cost']
            island_url = task['result']['islands'][0]['url']
            if island_name == 'No Islands':
                await bot.send_message(
                    task['chat_id'],
                    TEXT_ANSWER[task['language']]['no_island'],
                    reply_to_message_id=task['message_id'])
            elif task['min_turnip_cost'] > 0:
                await bot.send_message(
                    task['chat_id'],
                    TEXT_ANSWER[task['language']]['completed_task_cost'].format(
                        island_name,
                        island_dsc,
                        turnip_cost,
                        island_url),
                    parse_mode="HTML",
                    reply_to_message_id=task['message_id'])
            elif task['min_turnip_cost'] == 0:
                sender_text = await _create_islands_text(task['result']['islands'], task['language'])
                await bot.send_message(
                    task['chat_id'],
                    sender_text,
                    parse_mode="HTML",
                    reply_to_message_id=task['message_id'])