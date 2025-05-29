from pyrogram import Client, filters , enums
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton
from info import ADMINS, START_IMG, URL
import re
from database.users_chats_db import db
@Client.on_message(filters.command("post_mode") & filters.user(ADMINS))
async def update_post_mode(client, message):
    try:
        post_mode = await db.update_post_mode_handle()
        btn = [[
        InlineKeyboardButton("ᴘᴏsᴛ ᴍᴏᴅᴇ ➜", callback_data="update_post_mode"),
        InlineKeyboardButton(f"{'sɪɴɢʟᴇ' if post_mode.get('singel_post_mode', True) else 'ᴍᴜʟᴛɪ'} ᴍᴏᴅᴇ", callback_data="change_update_post_mode"),
    ],
    [
        InlineKeyboardButton("ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ ➜", callback_data="update_post_mode"),
        InlineKeyboardButton(f"{'ᴀʟʟ' if post_mode.get('all_files_post_mode', True) else 'ɴᴇᴡ'} ғɪʟᴇs", callback_data="all_files_post_mode"),
    ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await message.reply_photo(caption="<b>sᴇʟᴇᴄᴛ ᴘᴏsᴛ ᴍᴏᴅᴇ ғʀᴏᴍ ʙᴇʟᴏᴡ :</b>", photo=START_IMG, reply_markup=reply_markup)
    except Exception as e:
        print('Err in update_post_mode', e)

@Client.on_message(filters.command("set_muc") & filters.user(ADMINS))
async def set_muc_id(client, message):
    try:
        id = message.command[1]
        if id:
            is_suc = await db.movies_update_channel_id(int(id))
            if is_suc:
                await message.reply("Successfully set movies update  channel id : " + id)
            else:
                await message.reply("Failed to set movies update channel id : " + id)
        else:
            await message.reply("Invalid channel id : " + id)
    except Exception as e:
        print('Err in set_muc_id', e)
        await message.reply("Failed to set movies channel id!")

@Client.on_message(filters.command("del_muc") & filters.user(ADMINS))
async def del_muc_id(client, message):
    try:
        is_suc = await db.del_movies_channel_id()
        if is_suc:
            await message.reply("Successfully deleted movies channel id")
        else:
            await message.reply("Failed to delete movies channel id")
    except Exception as e:
        print('Err in del_muc_id', e)
        await message.reply("Failed to delete movies channel id!")

@Client.on_message(filters.command("url"))
async def give_url(bot, message):
    if URL != None:
        bot_url = URL
        await message.reply(f'Here is your Bot\'s F2L URL\n{bot_url}\nAur yeh original URL\nhttps://n2movies.koyeb.app/')
    else:
        await message.reply(f'Bro you have not provided the URL in enviroment')

@Client.on_message(filters.command("vjcmds"))
async def give_vjcmds(bot, message):
    await message.reply("""VJ ki repo ke imp. cmds yeh rahe
/users - 𝑡𝑜 𝑔𝑒𝑡 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑚𝑦 𝑢𝑠𝑒𝑟𝑠 𝑎𝑛𝑑 𝑖𝑑𝑠.
/chats - 𝑡𝑜 𝑔𝑒𝑡 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑡ℎ𝑒 𝑚𝑦 𝑐ℎ𝑎𝑡𝑠 𝑎𝑛𝑑 𝑖𝑑𝑠 
/leave  - 𝑡𝑜 𝑙𝑒𝑎𝑣𝑒 𝑓𝑟𝑜𝑚 𝑎 𝑐ℎ𝑎𝑡.
/disable  -  𝑑𝑜 𝑑𝑖𝑠𝑎𝑏𝑙𝑒 𝑎 𝑐ℎ𝑎𝑡.
/enable - 𝑟𝑒-𝑒𝑛𝑎𝑏𝑙𝑒 𝑐ℎ𝑎𝑡.
/set_template - 𝑇𝑜 𝑠𝑒𝑡 𝑎 𝑐𝑢𝑠𝑡𝑜𝑚 𝐼𝑀𝐷𝑏 𝑡𝑒𝑚𝑝𝑙𝑎𝑡𝑒 𝑓𝑜𝑟 𝑖𝑛𝑑𝑖𝑣𝑖𝑑𝑢𝑎𝑙 𝑔𝑟𝑜𝑢𝑝𝑠
/gfilter - 𝑇𝑜 𝑎𝑑𝑑 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠.
/gfilters - 𝑇𝑜 𝑣𝑖𝑒𝑤 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑎𝑙𝑙 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠.
/delg - 𝑇𝑜 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎 𝑠𝑝𝑒𝑐𝑖𝑓𝑖𝑐 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟.
/delallg - 𝑇𝑜 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎𝑙𝑙 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠 𝑓𝑟𝑜𝑚 𝑡ℎ𝑒 𝑏𝑜𝑡'𝑠 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒.
/deletefiles - 𝑇𝑜 𝑑𝑒𝑙𝑒𝑡𝑒 𝑃𝑟𝑒𝐷𝑉𝐷 𝑎𝑛𝑑 𝐶𝑎𝑚𝑅𝑖𝑝 𝐹𝑖𝑙𝑒𝑠 𝑓𝑟𝑜𝑚 𝑡ℎ𝑒 𝑏𝑜𝑡'𝑠 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒.
/restart  - 𝑟𝑒𝑠𝑡𝑎𝑟𝑡 𝑡ℎ𝑒 𝑏𝑜𝑡 𝑠𝑒𝑟𝑣𝑒𝑟
/fsub - 𝑎𝑑𝑑 𝑓𝑜𝑟𝑐𝑒 𝑠𝑢𝑏𝑠𝑐𝑟𝑖𝑏𝑒 𝑐ℎ𝑎𝑛𝑛𝑒𝑙 𝑖𝑛 𝑔𝑟𝑜𝑢𝑝
/nofsub - 𝑟𝑒𝑚𝑜𝑣𝑒 𝑜𝑟 𝑜𝑓𝑓 𝑓𝑜𝑟𝑐𝑒 𝑠𝑢𝑏𝑠𝑐𝑟𝑖𝑏𝑒 𝑖𝑛 𝑦𝑜𝑢𝑟 𝑔𝑟𝑜𝑢𝑝
/stream - 𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒 𝑠𝑡𝑟𝑒𝑎𝑚 𝑎𝑛𝑑 𝑑𝑜𝑤𝑛𝑙𝑜𝑎𝑑 𝑙𝑖𝑛𝑘 𝑜𝑓 𝑦𝑜𝑢𝑟 𝑓𝑖𝑙𝑒
/stickerid - 𝑡𝑜 𝑔𝑒𝑡 𝑖𝑑 𝑎𝑛𝑑 𝑢𝑛𝑖𝑞𝑢𝑒 𝐼'𝑑 𝑜𝑓 𝑠𝑡𝑖𝑐𝑘𝑒𝑟
/font - 𝑡𝑜 𝑔𝑒𝑡 𝑎𝑛𝑦 𝑡𝑦𝑝𝑒 𝑜𝑓 𝑓𝑜𝑛𝑡 𝑜𝑓 𝑎𝑛𝑦 𝑤𝑜𝑟𝑑
/purgerequests - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎𝑙𝑙 𝑗𝑜𝑖𝑛 𝑟𝑒𝑞𝑢𝑒𝑠𝑡𝑠 𝑓𝑟𝑜𝑚 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒
/totalrequests - 𝑔𝑒𝑡 𝑡𝑜𝑡𝑎𝑙 𝑛𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑗𝑜𝑖𝑛 𝑟𝑒𝑞𝑢𝑒𝑠𝑡 𝑓𝑟𝑜𝑚 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒""")

