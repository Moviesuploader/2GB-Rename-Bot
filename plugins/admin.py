from config import Config
from helper.database import db
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os, sys, time, asyncio, logging, datetime
from helper.utils import humanbytes
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@Client.on_message(filters.command("stats") & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    db.botdata(int(botid))
    data = db.get_user_data(int(botid))
    total_rename = data["total_rename"]
    total_size = data["total_size"]
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))    
    start_t = time.time()
    st = await message.reply('**Accessing The Bot Details...**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bot Status--**\n\n**⌚️ Bot Uptime :- `{uptime}`\n🐌 Current Ping :- `{time_taken_s:.3f} MS` \n👭 Total Users 📊 :- `{total_users}`\n✍🏻 Total Renamed Files :- {total_rename}\n🔢 Total Renamed Size :- {humanbytes(int(total_size))}**")

#Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("**🔄 Restarting...**")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"**{m.from_user.mention} or {m.from_user.id} is Started The Broadcast 💌...**")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("**Broadcast 💌 Started...!**") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"**Broadcast 💌 in Progress :-\nTotal Users 📊 :- {total_users}\nCompleted :- {done} / {total_users}\nSuccess :- {success}\nFailed :- {failed}**")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"**Broadcast Completed...\nCompleted in :- `{completed_in}`.\n\nTotal Users 📊 :- {total_users}\nCompleted :- {done} / {total_users}\nSuccess :- {success}\nFailed :- {failed}**")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} :- Deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} :- Blocked The Bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} :- User ID Invalid")
        return 400
    except Exception as e:
        logger.error(f"{user_id} :- {e}")
        return 500
 
