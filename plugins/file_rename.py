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
import os
import time
import shutil
import json
import shlex
from plugins.utils import get_media_file_name, get_file_attr, rm_dir, execute
from config import Config

LOG_CHANNEL = Config.LOG_CHANNEL

#def get_ffprobe_path():
#    return os.path.abspath("./bin/ffprobe.exe")

@Client.on_message(filters.command("change_mode") & filters.private & filters.incoming)
async def set_mode(client, message):
    upload_mode = await db.get_upload_mode(message.from_user.id)
    if upload_mode:
        await db.set_upload_mode(message.from_user.id, False)
        text = f"**From Now all Files will be Uploaded as Files {FILE_FOLDER}**"
    else:
        await db.set_upload_mode(message.from_user.id, True)
        text = f"**From Now all Files will be Uploaded as Video ð¥**"
    await message.reply_text(text, quote=True)

@Client.on_message(filters.command("get_mode") & filters.private & filters.incoming)
async def get_mode(client, message):
    user_id = message.from_user.id
    upload_mode = await db.get_upload_mode(user_id)

    if upload_mode:
        text = "**Your current Upload mode :- Video Mode ð¥**"
    else:
        text = "**Your Current Upload mode :- File Mode ð**"

    await message.reply_text(text, quote=True)

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    mention = message.from_user.mention
    if file.file_size > 2000 * 1024 * 1024:
        await message.reply_text(f"**Sorry {mention} This Bot Doesn't Support Uploading Files Bigger Than 2GB. You Can Use [4GB Rename Star Bots](https://t.me/Star_4GB_Rename_Bot)**")
        return

    try:
        await message.reply_text(
            text=f"**Please Enter New File Name...\n\nOld File Name :-** `{filename}`",
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True)
        )
        await sleep(30)
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(
            text=f"**Please Enter New File Name...\n\nOld File Name :-** `{filename}`",
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True)
        )
    except:
        pass
        
@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_filename = message.text[:60]
        file_caption = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not ".m" in new_filename:
            extn = media.file_name.rsplit('.', 1)[-1] if "." in media.file_name else "mkv"
            new_filename = f"{new_filename}.{extn}"
        if not any(ext in file_caption for ext in [".mp4", ".mkv"]):
            extn = media.file_name.rsplit('.', 1)[-1] if "." in media.file_name else "mkv"
            file_caption = f"{file_caption}.{extn}"
        await reply_message.delete()
        file_path = f"downloads/{new_filename}"
        upload_mode = await db.get_upload_mode(message.from_user.id)
        ms = await message.reply_text("**Trying to Ã°ÂÂÂ¥ Downloading...**")
        try:
            path = await client.download_media(
                message=file, file_name=f"downloads/{new_filename}",
                progress=progress_for_pyrogram, progress_args=("<b>Ã°ÂÂÂ¥ Downloading...</b>", ms, time.time())
            )
        except Exception as e:
            await ms.edit(str(e))
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

        title = "StarMovies.hop.sh"
        subtitle_title = "StarMovies.hop.sh"
        audio_title = "StarMovies.hop.sh"
        video_title = "StarMovies.hop.sh"

        if c_caption:
            try:
                caption = c_caption.format(
                    filename=file_caption, filesize=humanbytes(media.file_size), duration=convert(duration)
                )
            except Exception as e:
                return await ms.edit(text=f"**Your Caption Error Except Keyword Argument ({e})**")
        else:
            caption = f"**{file_caption}**"

        if media.thumbs or c_thumb:
            if c_thumb:
                ph_path = await client.download_media(c_thumb)
            else:
                ph_path = await client.download_media(media.thumbs[0].file_id)
                Image.open(ph_path).convert("RGB").save(ph_path)
                img = Image.open(ph_path)
                img.resize((320, 320))
                img.save(ph_path, "JPEG")

        await ms.edit("**Trying to Ã°ÂÂÂ¤ Uploading...**")
        #ffprobe_path = client.get_ffprobe_path()
        output = await execute(f"ffprobe -hide_banner -show_streams -print_format json {shlex.quote(path)}")

        if not output:
            await rm_dir(path)
            return await ms.edit("**Can't fetch media info!**")

        try:
            details = json.loads(output[0])
            middle_cmd = f"ffmpeg -i {shlex.quote(file_path)} -c copy -map 0"

            if title:
                middle_cmd += f' -metadata title="{title}"'

            for stream_index, stream in enumerate(details["streams"]):
                if stream["codec_type"] == "video" and video_title:
                    middle_cmd += f' -metadata:s:{stream_index} title="{video_title}"'
                elif stream["codec_type"] == "audio" and audio_title:
                    middle_cmd += f' -metadata:s:{stream_index} title="{audio_title}"'
                elif stream["codec_type"] == "subtitle" and subtitle_title:
                    middle_cmd += f' -metadata:s:{stream_index} title="{subtitle_title}"'

            middle_cmd += f" {shlex.quote(file_path)}"
            await execute(middle_cmd)

            if upload_mode:
                await client.send_video(
                    chat_id=message.chat.id, video=file_path, caption=caption, thumb=ph_path,
                    duration=duration, progress=progress_for_pyrogram,
                    progress_args=("<b>Ã°ÂÂÂ¤ Uploading...</b>", ms, time.time())
                )

                await client.send_video(
                    chat_id=LOG_CHANNEL, video=file_path, caption=caption,
                    thumb=ph_path, duration=duration
                )
            else:
                await client.send_document(
                    chat_id=message.chat.id, document=file_path, thumb=ph_path,
                    caption=caption, progress=progress_for_pyrogram,
                    progress_args=("<b>Ã°ÂÂÂ¤ Uploading...</b>", ms, time.time())
                )

                await client.send_document(
                    chat_id=LOG_CHANNEL, document=file_path, thumb=ph_path, caption=caption
                )
        except Exception as e:
            os.remove(path)
            await ms.edit(f"**Error: {e}**")
            return

        await ms.delete()
        os.remove(path)
