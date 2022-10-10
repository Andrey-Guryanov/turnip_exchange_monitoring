import os
from aiogram import Bot
from dotenv import load_dotenv
from modules.answer_txt_creator import get_text_answer

try:
    from common_modules.app_settings import load_settings
    from common_modules.model_mongo import Mongo_db
except ModuleNotFoundError:
    import sys
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    from common_modules.app_settings import load_settings
    from common_modules.model_mongo import Mongo_db


load_dotenv()

try:
    TEXT_ANSWER = get_text_answer('./sys/text_answer.json')
except FileNotFoundError:
    TEXT_ANSWER = get_text_answer('../sys/text_answer.json')

SETTINGS = load_settings()

TELEGRAM_TOKEN=os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
mongo_db = Mongo_db(SETTINGS['db_name'])