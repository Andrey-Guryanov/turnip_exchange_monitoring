import os
from pathlib import Path

try:
    from common_modules.app_settings import load_settings
    from common_modules.model_mongo import Mongo_db
except ModuleNotFoundError:
    import sys
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    from common_modules.app_settings import load_settings
    from common_modules.model_mongo import Mongo_db

ISLAND_CLASS = {
    'island_blocks': 'relative items-center w-56 row-gap-1 pb-4 bg-center select-none note bg-background sm:w-64',
    'island_name': 'text-2xl leading-9 text-center font-poster md:text-4xl',
    'island_turnip_cost': 'ml-2',
    'island_description': 'p-4 pt-0 overflow-hidden text-xs whitespace-pre-wrap justify-self-stretch',
    'island_description_paid': 'p-4 pt-0 overflow-hidden text-xs whitespace-pre-wrap justify-self-stretch themed-background',
    'island_queue': 'col-start-2 mr-1 text-xs italic justify-self-end',
    'island_rating': 'font-bold text-foreground text-2xs'}

ISLAND_URL = 'https://turnip.exchange/islands'
ISLAND_ELEMENT_XPATH = '//*[@id="app"]/div[2]/div[2]/div[1]'
LOG_PATH = Path.cwd() / 'logs'

SETTINGS = load_settings()

DRIVER_PATH = './firefox_driver/geckodriver'

mongo_db = Mongo_db(SETTINGS['db_name'])