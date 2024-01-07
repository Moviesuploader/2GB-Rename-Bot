import os
import time
import json
import shlex
import shutil
from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.metadata.file_info import get_media_file_name, get_file_attr
from plugins.metadata.rm import rm_dir
from plugins.metadata.executor import execute
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db

@Client.on_message(filters.command("video_info") & filters.private)
async def video_info_handler(c: Client, m: Message):
    if not m.reply_to_message or len(m.command) == 1:
        await m.reply_text(
            "Reply to a video with /video_info to change the title, subtitle_title, audio_title, and video_title to 'StarMovies.hop.sh'.",
            True
        )
        return

    file_type = m.reply_to_message.video or m.reply_to_message.document
    if not file_type:
        await m.reply_text("This is not a Video or Document!", True)
        return

    title = "StarMovies.hop.sh"
    subtitle_title = "StarMovies.hop.sh"
    audio_title = "StarMovies.hop.sh"
    video_title = "StarMovies.hop.sh"

    editable = await m.reply_text("Downloading Video...", quote=True)
    dl_loc = "./Downloads" + "/" + str(m.from_user.id) + "/" + str(m.message_id) + "/"
    root_dl_loc = dl_loc
    if not os.path.isdir(dl_loc):
        os.makedirs(dl_loc)

    c_time = time.time()
    the_media = await c.download_media(
        message=m.reply_to_message,
        file_name=dl_loc,
        progress=progress_for_pyrogram,
        progress_args=(
            "Downloading...",
            editable,
            c_time
        )
    )

    await editable.edit("Trying to Fetch Media Metadata...")

    output = await execute(f"ffprobe -hide_banner -show_streams -print_format json {shlex.quote(the_media)}")

    if not output:
        await rm_dir(root_dl_loc)
        return await editable.edit("Can't fetch media info!")

    try:
        details = json.loads(output[0])
        middle_cmd = f"ffmpeg -i {shlex.quote(the_media)} -c copy -map 0"

        if title:
            middle_cmd += f' -metadata title="{title}"'

        for stream in details["streams"]:
            if (stream["codec_type"] == "video") and video_title:
                middle_cmd += f' -metadata:s:{stream["index"]} title="{video_title}"'
            elif (stream["codec_type"] == "audio") and audio_title:
                middle_cmd += f' -metadata:s:{stream["index"]} title="{audio_title}"'
            elif (stream["codec_type"] == "subtitle") and subtitle_title:
                middle_cmd += f' -metadata:s:{stream["index"]} title="{subtitle_title}"'

        dl_loc = dl_loc + str(time.time()).replace(".", "") + "/"

        if not os.path.isdir(dl_loc):
            os.makedirs(dl_loc)

        middle_cmd += f" {shlex.quote(dl_loc + get_media_file_name(m.reply_to_message))}"
        await editable.edit("Please Wait...\n\nProcessing Video...")
        await execute(middle_cmd)
        await editable.edit("Renamed Successfully!")
    except:
        await editable.edit("Failed to process video!")
        await rm_dir(root_dl_loc)
        return

    try:
        os.remove(the_media)
    except:
        pass

    upload_mode = await db.get_upload_mode(m.from_user.id)
    _default_thumb_ = await db.get_thumbnail(m.from_user.id)

    if not _default_thumb_:
        _m_attr = get_file_attr(m.reply_to_message)
        _default_thumb_ = _m_attr.thumbs[0].file_id if (_m_attr and _m_attr.thumbs) else None

    if _default_thumb_:
        _default_thumb_ = await c.download_media(_default_thumb_, root_dl_loc)

    if (not upload_mode) and m.reply_to_message.video:
        await c.upload_video(
            chat_id=m.chat.id,
            video=f"{dl_loc}{get_media_file_name(m.reply_to_message)}",
            thumb=_default_thumb_ or None,
            editable_message=editable,
        )
    else:
        await c.upload_document(
            chat_id=m.chat.id,
            document=f"{dl_loc}{get_media_file_name(m.reply_to_message)}",
            editable_message=editable,
            thumb=_default_thumb_ or None
        )
    await rm_dir(root_dl_loc)
