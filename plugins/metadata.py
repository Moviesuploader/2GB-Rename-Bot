from pyrogram import Client, filters
from pyrogram.types import InputFile
from moviepy.editor import VideoFileClip
from io import BytesIO

@Client.on_message(filters.video)
def handle_video(client, message):
    try:
        chat_id = message.chat.id
        file_id = message.video.file_id

        # Download the video file
        video_file = client.download_media(file_id)

        # Edit metadata (example: set title)
        edited_video = edit_metadata(video_file, title="New Title")

        # Send the edited video back to the user
        client.send_video(chat_id, video=InputFile(BytesIO(edited_video)))

    except Exception as e:
        client.send_message(chat_id, f"Error: {e}")

def edit_metadata(video_file, title):
    # Load the video clip
    video_clip = VideoFileClip(BytesIO(video_file))

    # Edit metadata
    video_clip = video_clip.set("title", title)

    # Convert back to bytes
    edited_video = BytesIO()
    video_clip.write_videofile(edited_video, codec="libx264", audio_codec="aac")

    return edited_video.getvalue()
