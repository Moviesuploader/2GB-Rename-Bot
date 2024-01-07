import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "11973721")
    API_HASH  = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6157557700:AAG90-whhrmQeVPWRIc9RNmkk6J0CeEIOfo") 
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","Rename-Star-Bot")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://KarthikMovies:KarthikUK007@cluster0.4l5byki.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://graph.org/file/1412d9f93d77c350d8268.jpg")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1391556668 5162208212').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Star_Bots_Tamil") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001821439025"))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))

class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hello 👋🏻 {} ❤️,\nI'm An Star Bots Tamil's Official Rename Bot. This is An Advanced and Yet Powerful Rename Bot.\nFor More Details Check /help\n\n➠ You Can Rename File / Video.\n➠ Change Thumbnail of Your File / Video.\n➠ Convert Video to File & File to Video.\nOur Bot Fully customisable\n➠ Permanent Thumbnail 🖼️ and Custom Caption ✍🏻.\n\nMaintenance By :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)</b>"""

    ABOUT_TXT = """<b>🤖 My Name :- {}\n
🧑🏻‍💻 Developer :- <a href=https://t.me/TG_Karthik><b>Karthik</b></a>\n
💁🏻 My Best Friend :- {}\n
📝 Language :- Python3\n
📚 Framework :- Pyrogram\n
📡 Hosted on :- VPS\n
💾 Database :- <a href=https://cloud.mongodb.com/>Mongo DB</a>\n
🎥 Movie Updates :- <a href=https://t.me/Star_Moviess_Tamil><b></b>Star Movies Tamil</a>\n
🤖 Bot Channel :- <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b>"""

    HELP_TXT = """**--Available Commands--
    
    ➠ /start :- Check if 😊 I'm Alive
    ➠ /help :- How to Use❓
    ➠ /about :- to Know About Me 😌
    
    🖼️ --How to Set Thumbnail--
    
    ➠ /start The Our Bot And Send Any Photo to Automatically Set Thumbnail 🖼️
    ➠ /showthumbnail :- View Current Thumbnail 🖼️
    ➠ /deletethumbnail :- Delete 🗑️ Your Thumbnail 🖼️
    
    ✍🏻 --How to Set Custom Caption--
    
    ➠ /set_caption :- Set Custom Caption ✍🏻
    ➠ /see_caption :- View Current Caption ✍🏻
    ➠ /del_caption :- Delete 🗑️ Your Caption
    Example :- `/set_caption <b>📁 File Name :- {filename}\n\n💾 File Size :- {filesize}\n\n⏰ Duration :- {duration}</b>`
    
    `/set_caption <b>{filename}</b>`
    
    --How to Change Upload Mode--
    
    ➠ /change_mode :- Change Your Upload Mode (File or Video)
    ➠ /get_mode :- Get Current Upload Mode
    
    ✏️ --How to Rename File--
    
    ➠ Send me Any File And Type New File Name
    
    --📂 Supported File Formats--
    
    ➠ 📁 Document
    ➠ 🎥 Video
    ➠ 🎵 Audio
    
    ⚠️ Contact For Any Problem :- [👥 Support Group](https://t.me/Star_Bots_Tamil_Support)**"""
    
    HELP_TEXT = "**--Available Commands--\n\n➠ /start :- Check if 😊 I'm Alive\n➠ /help :- How to Use❓\n➠ /about :- to Know About Me 😌\n\n🖼️ --How to Set Thumbnail--\n\n➠ /start The Our Bot And Send Any Photo to Automatically Set Thumbnail 🖼️\n➠ /showthumbnail :- View Current Thumbnail 🖼️\n➠ /deletethumbnail :- Delete 🗑️ Your Thumbnail 🖼️\n\n✍🏻 --How to Set Custom Caption--\n\n➠ /set_caption :- Set Custom Caption ✍🏻\n➠ /see_caption :- View Current Caption ✍🏻\n➠ /del_caption :- Delete 🗑️ Your Caption\nExample :- `/set_caption <b>📁 File Name :- {filename}\n\n💾 File Size :- {filesize}\n\n⏰ Duration :- {duration}</b>`\n\n `/set_caption <b>{filename}</b>`\n\n--How to Change Upload Mode--\n\n➠ /change_mode :- Change Your Upload Mode (File or Video)\n➠ /get_mode :- Get Current Upload Mode\n\n✏️ --How to Rename File--\n\n➠ Send me Any File And Type New File Name\n\n--📂 Supported File Formats--\n\n➠ 📁 Document\n➠ 🎥 Video\n➠ 🎵 Audio\n\n⚠️ Contact For Any Problem :- [👥 Support Group](https://t.me/Star_Bots_Tamil_Support)**"

    DEV_TXT = """<b><u>Special Thanks & Developer</b></u>
**You Can pay Any Our Bot's Repo. If you're able to Donate or Buy Our Bot's Repo, please Consider using these Methods:

UPI ID :- `starbotstamil@upi`

GPay :- `starbotstamil@oksbi`

Phonepe :- `starbotstamil@ybl`

Paytm :- `starbotstamil@paytm`

After pay Must Send Screenshot Admin**

<b>🧑🏻‍💻 Developer :- </b><a href=https://t.me/TG_Karthik><b>Karthik</b></a>
**Contact me for more info**"""

    PROGRESS_BAR = """<b>\n
🚀 Speed :- {3}/sec\n
💯 Percentage :- {0}%\n
✅ Done :- {1}\n
💾 Size :- {2}\n
⏰ Time Left :- {4}\n
©️ [Star Bots Tamil](https://t.me/Star_Bots_Tamil)</b>"""
