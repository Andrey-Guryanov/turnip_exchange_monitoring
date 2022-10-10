import os
from time import time
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_HOST = os.getenv('MONGO_HOST')


class Mongo_db(object):
    def __init__(self, db_name):
        if MONGO_USER and MONGO_PASS:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27018')
        else:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                f'mongodb://{MONGO_HOST}:27017')
        self.db = self.client[db_name]
        self.coll = None

    async def up_collection(self, coll_name):
        self.coll = await self.db[coll_name]

    async def find_user(self, chat_id):
        self.coll = self.db['bot_users']
        user = await self.coll.find_one(
            {"chat_id": chat_id})
        return user

    async def create_user(self, chat_id, username, language):
        new_user = {
            'chat_id': chat_id,
            'username': username,
            'language': language,
            'count_requests': 0, }
        self.coll = self.db['bot_users']
        await self.coll.insert_one(new_user)

    async def update_language_user(self, obj_id, language):
        self.coll = self.db['bot_users']
        await self.coll.update_one({"_id": obj_id}, {"$set": {"language": language}})

    async def _check_task_no_cost(self, chat_id):
        self.coll = self.db['tasks']
        task = await self.coll.find_one({"$and": [
            {"chat_id": chat_id}, {"min_turnip_cost": 0}]})
        return task

    async def _check_task_cost(self, chat_id):
        self.coll = self.db['tasks']
        task = await self.coll.find_one({"$and": [
            {"chat_id": chat_id}, {"min_turnip_cost": {'$gt': 0}}]})
        return task

    async def _update_task_cost(self, chat_id, new_cost):
        self.coll = self.db['tasks']
        await self.coll.update_one({"chat_id": chat_id}, {"$set": {"min_turnip_cost": new_cost}})

    async def add_task_no_cost(self, chat_id, min_turnip_cost, message_id, language):
        task = await self._check_task_no_cost(chat_id)
        self.coll = self.db['tasks']
        if task is None or task['min_turnip_cost'] != 0:
            new_task = {
                'chat_id': chat_id,
                'min_turnip_cost': min_turnip_cost,
                'create_dtt': time(),
                'status': 'waiting',
                'message_id': message_id,
                'language': language,
                'result': {}}
            await self.coll.insert_one(new_task)
            return True
        else:
            return False

    async def add_task_cost(self, chat_id, min_turnip_cost, message_id, language):
        task = await self._check_task_cost(chat_id)
        self.coll = self.db['tasks']
        if task is None:
            new_task = {
                'chat_id': chat_id,
                'min_turnip_cost': min_turnip_cost,
                'create_dtt': time(),
                'status': 'waiting',
                'message_id': message_id,
                'language': language,
                'result': {}}
            await self.coll.insert_one(new_task)
            return True
        else:
            await self._update_task_cost(task['chat_id'], min_turnip_cost)
            return False

    async def check_new_task(self):
        result = []
        self.coll = self.db['tasks']
        tasks = self.coll.find({'status': 'waiting'}).to_list(length=1000)
        for task in await tasks:
            result.append(task)
        return result

    async def task_completed(self, obj_id, result):
        self.coll = self.db['tasks']
        await self.coll.update_one({"_id": obj_id}, {"$set": {"status": "completed", 'result': result}})
        return True

    async def check_completed_task(self):
        self.coll = self.db['tasks']
        task = await self.coll.find_one_and_delete({'status': 'completed'})
        return task
