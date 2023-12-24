import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from helper.database import db
from config import Config, Txt  
  
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)                
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton("🧑🏻‍💻 Developer", callback_data='dev')
        ],[
        InlineKeyboardButton('🤖 Update Channel', url='https://t.me/Star_Bots_Tamil'),
        InlineKeyboardButton('👥 Support Group', url='https://t.me/Star_Bots_Tamil_Support')
        #],[
        #InlineKeyboardButton('⚙️ Settings', callback_data='showSettings')
        ],[
        InlineKeyboardButton('🎛️ About', callback_data='about'),
        InlineKeyboardButton('🛠️ Help', callback_data='help')
        ],[
        InlineKeyboardButton('🔒 Close', callback_data='close')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("help"))
async def help(client, message):
    user = message.from_user
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton("🧑🏻‍💻 Developer", callback_data='dev')
        ],[
        InlineKeyboardButton('🤖 Update Channel', url='https://t.me/Star_Bots_Tamil'),
        InlineKeyboardButton('👥 Support Group', url='https://t.me/Star_Bots_Tamil_Support')
        ],[
        InlineKeyboardButton('🎛️ About', callback_data='about'),
        InlineKeyboardButton('🏠 Home', callback_data='start')
        ],[
        InlineKeyboardButton('🔒 Close', callback_data='close')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.HELP_TEXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.HELP_TEXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("about"))
async def about(client, message):
    user = message.from_user
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton("🧑🏻‍💻 Developer", callback_data='dev')
        ],[
        InlineKeyboardButton('🤖 Update Channel', url='https://t.me/Star_Bots_Tamil'),
        InlineKeyboardButton('👥 Support Group', url='https://t.me/Star_Bots_Tamil_Support')
        ],[
        InlineKeyboardButton('🛠️ Help', callback_data='help'),
        InlineKeyboardButton('🏠 Home', callback_data='start')
        ],[
        InlineKeyboardButton('🔒 Close', callback_data='close')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.ABOUT_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.ABOUT_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("🧑🏻‍💻 Developer", callback_data='dev')
                ],[
                InlineKeyboardButton('🤖 Update Channel', url='https://t.me/Star_Bots_Tamil'),
                InlineKeyboardButton('👥 Support Group', url='https://t.me/Star_Bots_Tamil_Support')
                ],[
                InlineKeyboardButton('🎛️ About', callback_data='about'),
                InlineKeyboardButton('🛠️ Help', callback_data='help')
                ],[
                InlineKeyboardButton('🔒 Close', callback_data='close')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("🤖 Update Channel", url="https://t.me/Star_Bots_Tamil")
                ],[
                InlineKeyboardButton("👥 Support Group", url='https://t.me/Star_Bots_Tamil_Support')
                ],[
                InlineKeyboardButton("🎛️ About", callback_data = "about"),
                InlineKeyboardButton("🏠 Home", callback_data = "start")
                ],[
                InlineKeyboardButton('🔒 Close', callback_data='close')
            ]])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("🤖 Update Channel", url="https://t.me/Star_Bots_Tamil")
                ],[
                InlineKeyboardButton("👥 Support Group", url="https://t.me/Star_Bots_Tamil_Support")
                ],[
                InlineKeyboardButton("🛠️ Help", callback_data = "help"),
                InlineKeyboardButton("🏠 Home", callback_data = "start")
                ],[
                InlineKeyboardButton('🔒 Close', callback_data='close')
            ]])            
        )
    elif data == "dev":
        await query.message.edit_text(
            text=Txt.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("🤖 Update Channel", url="https://t.me/Star_Bots_Tamil")
                ],[
                InlineKeyboardButton("👥 Support Group", url="https://t.me/Star_Bots_Tamil_Support")
                ],[
                InlineKeyboardButton("🎛️ About", callback_data = "about"),
                InlineKeyboardButton("🏠 Home", callback_data = "start"),
                InlineKeyboardButton("🛠️ Help", callback_data = "help")
                ],[
                InlineKeyboardButton('🔒 Close', callback_data='close')
            ]])          
        )
    elif data == "deletethumbnail":
        user_id = query.from_user.id
        await db.set_thumbnail(user_id, file_id=None)
        await query.answer("❌️ Your Thumbnail Deleted Successfully 🗑️")
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
