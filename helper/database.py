import datetime
import motor.motor_asyncio
from config import Config
from .utils import send_log

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user

    def new_user(self, id):
        return dict(
            _id=int(id),
            upload_mode=False,
            file_id=None,
            caption=None
        )

    async def botdata(chat_id):
        bot_id = int(chat_id)
        try:
            bot_data = {"_id": bot_id, "total_rename": 0, "total_size": 0}
            dbcol.insert_one(bot_data)
        except:
            pass

    async def total_rename(chat_id, renamed_file):
        now = int(renamed_file) + 1
        dbcol.update_one({"_id": chat_id}, {"$set": {"total_rename": str(now)}})

    async def total_size(chat_id, total_size, now_file_size):
        now = int(total_size) + now_file_size
        dbcol.update_one({"_id": chat_id}, {"$set": {"total_size": str(now)}})
    
    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)            
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

    async def set_upload_mode(self, user_id, upload_mode):
        await self.col.update({'_id': int(user_id)}, {'$set': {'upload_mode': upload_mode}})

    async def get_upload_mode(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('upload_mode', False)

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

    async def get_user_data(self, id) -> dict:
        user = await self.col.find_one({'_id': int(id)})
        return user or None

db = Database(Config.DB_URL, Config.DB_NAME)




