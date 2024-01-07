import shlex
import asyncio
from typing import Tuple
from pyrogram.types import Message
import shutil
import aiofiles.os

async def execute(cmnd: str) -> Tuple[str, str, int, int]:
    """
    Execute a Command as Async.

    :param cmnd: Pass Command as String.
    """

    cmnds = shlex.split(cmnd)
    process = await asyncio.create_subprocess_exec(
        *cmnds,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)

def get_media_file_name(message: Message):
    """
    Pass Message object of audio or document or sticker or video or animation to get file_name.
    """

    media = message.audio or \
            message.document or \
            message.sticker or \
            message.video or \
            message.animation

    if media and media.file_name:
        return media.file_name
    else:
        return None


def get_media_file_size(message: Message):
    """
    Pass Message object of audio or document or photo or sticker or video or animation or voice or video_note to get file_size.
    """

    media = message.audio or \
            message.document or \
            message.photo or \
            message.sticker or \
            message.video or \
            message.animation or \
            message.voice or \
            message.video_note

    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_mime_type(message: Message):
    """
    Pass Message object of audio or document or video to get mime_type
    """

    media = message.audio or \
            message.document or \
            message.video
    
    if media and media.mime_type:
        return media.mime_type
    else:
        return None


def get_media_file_id(message: Message):
    """
    Pass Message object of audio or document or photo or sticker or video or animation or voice or video_note to get file_id.
    """

    media = message.audio or \
            message.document or \
            message.photo or \
            message.sticker or \
            message.video or \
            message.animation or \
            message.voice or \
            message.video_note

    if media and media.file_id:
        return media.file_id
    else:
        return None


def get_file_type(message: Message):
    if message.document:
        return "document"
    if message.video:
        return "video"
    if message.audio:
        return "audio"


def get_file_attr(message: Message):

    """
    Combine audio or video or document
    """

    media = message.audio or \
            message.video or \
            message.document

    return media


def get_thumb_file_id(message: Message):
    media = message.audio or \
            message.video or \
            message.document
    if media and media.thumbs:
        return media.thumbs[0].file_id
    else:
        return None

  async def rm_dir(root: str = f"./Downloads"):
    """
    Delete a Folder.

    :param root: Pass DIR Path
    """

    try:
        shutil.rmtree(root)
    except Exception as e:
        logging.getLogger(__name__).error(e)


async def rm_file(file_path: str):
    """
    Delete a File.

    :param file_path: Pass File Path
    """
    try:
        await aiofiles.os.remove(file_path)
    except:
        pass
