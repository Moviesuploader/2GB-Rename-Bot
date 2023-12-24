from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram.emoji import *
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from asyncio import sleep
from PIL import Image
import os, time
from config import Config

LOG_CHANNEL = Config.LOG_CHANNEL

@Client.on_message(filters.command("mode") & filters.private & filters.incoming)
async def set_mode(client, message):
    upload_mode = await db.get_upload_mode(message.from_user.id)
    if upload_mode:
        await db.set_upload_mode(message.from_user.id, False)
        text = f"**From Now all files will be Uploaded as Files {FILE_FOLDER}**"
    else:
        await db.set_upload_mode(message.from_user.id, True)
        text = f"**From Now all files will be Uploaded as Video {VIDEO_CAMERA}**"
    await message.reply_text(text, quote=True)

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    mention = message.from_user.mention
    if file.file_size > 2000 * 1024 * 1024:
         await message.reply_text("**Sorry {mention} This Bot is Doesn't Support Uploading Files Bigger Than 2GB. So you Can Use 4GB Rename Bot 👉🏻 [4GB Rename Star Bots](https://t.me/Star_4GB_Rename_Bot)**")
         return

    try:
        await message.reply_text(
            text=f"**__Please Enter New File Name...__\n\nOld File Name :-** `{filename}`",
            reply_to_message_id=message.id,  
            reply_markup=ForceReply(True)
        )       
        await sleep(30)
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(
            text=f"**__Please Enter New File Name...__\n\nOld File Name :-** `{filename}`",
            reply_to_message_id=message.id,  
            reply_markup=ForceReply(True)
        )
    except:
        pass

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_filename = message.text 
        await message.delete() 
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_filename:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_filename = new_filename + "." + extn
        await reply_message.delete()
        file_path = f"downloads/{new_filename}"

        # Get upload mode from db
        upload_mode = await db.get_upload_mode(message.from_user.id)

        # Determine the button based on the upload mode
        button_text = "🎥 Video" if upload_mode else "📂 Document"
        callback_data = "upload_video" if upload_mode else "upload_document"

        # Send document or video directly based on user input
        ms = await message.reply_text("**Trying to 📥 Downloading...**")
        try:
            path = await client.download_media(message=file, file_name=f"downloads/{new_filename}", progress=progress_for_pyrogram, progress_args=("**📥 Download Started...**", ms, time.time()))                    
        except Exception as e:
            await ms.edit(e)
            return

        duration = 0
        try:
            metadata = extractMetadata(createParser(path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except:
            pass

        ph_path = None
        user_id = int(message.chat.id) 
        c_caption = await db.get_caption(message.chat.id)
        c_thumb = await db.get_thumbnail(message.chat.id)

        if c_caption:
            try:
                caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
            except Exception as e:
                return await ms.edit(text=f"**Your Caption Error Except Keyword Argument ({e})**")             
        else:
            caption = f"**{new_filename}**"

        if (media.thumbs or c_thumb):
            if c_thumb:
                ph_path = await client.download_media(c_thumb) 
            else:
                ph_path = await client.download_media(media.thumbs[0].file_id)
                Image.open(ph_path).convert("RGB").save(ph_path)
                img = Image.open(ph_path)
                img.resize((320, 320))
                img.save(ph_path, "JPEG")

        await ms.edit("**Trying to 📤 Uploading...**")

        try:
            if upload_mode:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("**📤 Upload Status :-**", ms, time.time()))

                # Log the sent video to LOG_CHANNEL
                await client.send_video(
                    chat_id=LOG_CHANNEL,
                    video=file_path,
                    thumb=ph_path,
                    duration=duration,
                    caption=caption
                )
            else:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("**📤 Upload Status :-**", ms, time.time()))

                # Log the sent document to LOG_CHANNEL
                await client.send_document(
                    chat_id=LOG_CHANNEL,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption
                )
        except Exception as e:
            os.remove(path)
            await ms.edit(f"**Error :- {e}**")
            return

        await ms.delete() 
        os.remove(path)
