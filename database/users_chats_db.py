import re
from pymongo.errors import DuplicateKeyError
import motor.motor_asyncio
from pymongo import MongoClient
from sample_info import tempDict
from info import DATABASE_NAME, DATABASE_URI, CUSTOM_FILE_CAPTION, IMDB, IMDB_TEMPLATE, MELCOW_NEW_USERS, P_TTI_SHOW_OFF, SINGLE_BUTTON, SPELL_CHECK_REPLY, PROTECT_CONTENT, AUTO_DELETE, MAX_BTN, AUTO_FFILTER, MULTI_FSUB, SHORTLINK_API, SHORTLINK_URL, IS_SHORTLINK, TUTORIAL, IS_TUTORIAL, SECONDDB_URI, DEFAULT_POST_MODE
import time
import datetime

my_client = MongoClient(DATABASE_URI)
mydb = my_client["referal_user"]

async def referal_add_user(user_id, ref_user_id):
    user_db = mydb[str(user_id)]
    user = {'_id': ref_user_id}
    try:
        user_db.insert_one(user)
        return True
    except DuplicateKeyError:
        return False
    

async def get_referal_all_users(user_id):
    user_db = mydb[str(user_id)]
    return user_db.find()
    
async def get_referal_users_count(user_id):
    user_db = mydb[str(user_id)]
    count = user_db.count_documents({})
    return count
    

async def delete_all_referal_users(user_id):
    user_db = mydb[str(user_id)]
    user_db.delete_many({}) 

    
class Database:

    default_setgs = {
        'button': SINGLE_BUTTON,
        'botpm': P_TTI_SHOW_OFF,
        'file_secure': PROTECT_CONTENT,
        'imdb': IMDB,
        'spell_check': SPELL_CHECK_REPLY,
        'welcome': MELCOW_NEW_USERS,
        'auto_delete': AUTO_DELETE,
        'auto_ffilter': AUTO_FFILTER,
        'max_btn': MAX_BTN,
        'template': IMDB_TEMPLATE,
        'caption': CUSTOM_FILE_CAPTION,
        'shortlink': SHORTLINK_URL,
        'shortlink_api': SHORTLINK_API,
        'is_shortlink': IS_SHORTLINK,
        'tutorial': TUTORIAL,
        'is_tutorial': IS_TUTORIAL,
        'fsub': MULTI_FSUB,
    }
    
    def __init__(self, database_name):
        #primary db 
        self._client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.users = self.db.uersz
        self.movies_update_channel = self.db.movies_update_channel
        self.update_post_mode = self.db.update_post_mode
        #secondary db
        self._client2 = motor.motor_asyncio.AsyncIOMotorClient(SECONDDB_URI)
        self.db2 = self._client2[database_name]
        self.col2 = self.db2.users
        self.grp2 = self.db2.groups


    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            file_id=None,
            caption=None,
            message_command=None,
            save=False,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )


    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
            settings=self.default_setgs
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        if tempDict['indexDB'] == DATABASE_URI:
            await self.col.insert_one(user)
        else:
            await self.col2.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        if not user:
            user = await self.col2.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = ((await self.col.count_documents({}))+(await self.col2.count_documents({})))
        return count

    async def get_bot(self, bot_id):
        bot_data = await self.bot.find_one({"bot_id": bot_id})
        return bot_data

    async def update_bot(self, bot_id, bot_data):
        await self.bot.update_one({"bot_id": bot_id}, {"$set": bot_data}, upsert=True)

    async def get_all_bots(self):
        return self.bot.find({})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        if not user:
            await self.col2.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
        else:
            await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        user = await self.col.find_one({'id': int(user_id)})
        if not user:
            await self.col2.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})
        else:
            await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            user = await self.col2.find_one({'id':int(id)})
            if not user:
                return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return ((await (self.col.find({})).to_list(length=None))+(await (self.col2.find({})).to_list(length=None)))
    

    async def delete_user(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            await self.col.delete_many({'id': int(user_id)})
        else:
            await self.col2.delete_many({'id': int(user_id)})


    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        users = self.col2.find({'ban_status.is_banned': True})
        chats = self.grp2.find({'chat_status.is_disabled': True})
        b_chats += [chat['id'] async for chat in chats]
        b_users += [user['id'] async for user in users]
        return b_users, b_chats
    


    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        if tempDict['indexDB'] == DATABASE_URI:
            await self.grp.insert_one(chat)
        else:
            await self.grp2.insert_one(chat)
    

    async def get_chat(self, id):
        chat = await self.grp.find_one({'id':int(id)})
        if not chat:
            chat = await self.grp2.find_one({'id':int(id)})
        return False if not chat else chat.get('chat_status')
    

    async def re_enable_chat(self, id):
        chat_status=dict(
            is_disabled=False,
            reason="",
            )
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        else:
            await self.grp2.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        
    async def update_settings(self, id, settings):
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
        else:
            await self.grp2.update_one({'id': int(id)}, {'$set': {'settings': settings}})
        
    
    async def get_settings(self, id):
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', self.default_setgs)
        else:
            chat = await self.grp2.find_one({'id':int(id)})
            if chat:
                return chat.get('settings', default)
        return self.default_setgs
    

    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(
            is_disabled=True,
            reason=reason,
            )
        chat = await self.grp.find_one({'id':int(chat)})
        if chat:
            await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
        else:
            await self.grp2.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
    

    async def total_chat_count(self):
        count = (await self.grp.count_documents({}))+(await self.grp2.count_documents({}))
        return count
    

    async def get_all_chats(self):
        return ((await (self.grp.find({})).to_list(length=None))+(await (self.grp2.find({})).to_list(length=None)))

    async def get_user(self, user_id):
        user_data = await self.users.find_one({"id": user_id})
        return user_data
            
    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                # User previously used the free trial, but it has ended.
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                await self.users.update_one({"id": user_id}, {"$set": {"expiry_time": None}})
        return False
    
    async def check_remaining_uasge(self, userid):
        user_id = userid
        user_data = await self.get_user(user_id)        
        expiry_time = user_data.get("expiry_time")
        # Calculate remaining time
        remaining_time = expiry_time - datetime.datetime.now()
        return remaining_time

    async def get_free_trial_status(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            return user_data.get("has_free_trial", False)
        return False

    async def give_free_trail(self, userid):        
        user_id = userid
        seconds = 5*60         
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {"id": user_id, "expiry_time": expiry_time, "has_free_trial": True}
        await self.users.update_one({"id": user_id}, {"$set": user_data}, upsert=True)
    
    
    async def all_premium_users(self):
        count = await self.users.count_documents({
        "expiry_time": {"$gt": datetime.datetime.now()}
        })
        return count

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None)

    async def set_msg_command(self, id, com):
        await self.col.update_one({'id': int(id)}, {'$set': {'message_command': com}})

    async def get_msg_command(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('message_command', None)

    async def set_save(self, id, save):
        await self.col.update_one({'id': int(id)}, {'$set': {'save': save}})

    async def get_save(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('save', False) 
    
    async def movies_update_channel_id(self , id=None):
        if id is None:
            myLinks = await self.movies_update_channel.find_one({})
            if myLinks is not None:
                return myLinks.get("id")
            else:
                return None
        return await self.movies_update_channel.update_one({} , {'$set': {'id': id}} , upsert=True)

    async def del_movies_channel_id(self):
        try: 
            isDeleted = await self.movies_update_channel.delete_one({})
            if isDeleted.deleted_count > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Got err in db set : {e}")
            return False
    async def update_post_mode_handle(self, index=0):
        post_mode = await self.update_post_mode.find_one({})
        if post_mode is None:
            post_mode = DEFAULT_POST_MODE
        if index == 1:
            post_mode["singel_post_mode"] = not post_mode.get("singel_post_mode", True)
        elif index == 2:
            post_mode["all_files_post_mode"] = not post_mode.get("all_files_post_mode", True)
        
        await self.update_post_mode.update_one({}, {"$set": post_mode}, upsert=True)
        
        return post_mode

db = Database(DATABASE_NAME)
