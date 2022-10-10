import asyncio
from time import sleep
from operator import itemgetter
from apps.user_agent import get_user_agent
from apps.selenium_browser import get_content
from apps.html_parser import html_parser
from constants import ISLAND_URL, ISLAND_ELEMENT_XPATH, DRIVER_PATH, mongo_db


def run_island_parser(driver_path: str) -> list:
    user_agent = get_user_agent()
    page_content = get_content(user_agent, ISLAND_URL, ISLAND_ELEMENT_XPATH, driver_path)
    islands = html_parser(page_content)
    return islands


async def handling_all_islands(waiting_task, islands, completed_tasks):
    for task in waiting_task:
        if task['min_turnip_cost'] == 0:
            await mongo_db.task_completed(task['_id'], {'islands': islands})
            completed_tasks.append(task['_id'])
    return completed_tasks


async def handling_cost_islands(waiting_task, island, completed_tasks):
    if island['name'] != 'No Islands':
        if island['queue']['count_waiting'] <= 5:
            for task in waiting_task:
                if (island['turnip_cost'] >= task['min_turnip_cost']
                        and task['_id'] not in completed_tasks):
                    await mongo_db.task_completed(task['_id'], {'islands': [island, ]})
                    completed_tasks.append(task['_id'])
    return completed_tasks


async def main() -> None:
    completed_tasks = []
    while True:
        waiting_task = await mongo_db.check_new_task()
        if len(waiting_task) > 0:
            islands = run_island_parser(DRIVER_PATH)
            islands = sorted(islands, key=itemgetter('turnip_cost'), reverse=True)
            if len(islands) > 0:
                completed_tasks = await handling_all_islands(
                    waiting_task, islands, completed_tasks)

                for island in islands:
                    completed_tasks = await handling_cost_islands(
                        waiting_task, island, completed_tasks)
        sleep(30)


if __name__ == '__main__':
    asyncio.run(main())
