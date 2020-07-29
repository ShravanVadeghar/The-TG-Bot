from telethon import events
import asyncio
from datetime import datetime
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from uniborg.util import admin_cmd


muted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=True,
    send_gifs=None,
    send_games=True,
    send_inline=None,
    embed_links=None
    )

@borg.on(admin_cmd("(demote) ?(.*)"))
async def _(event):
	
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "demote":
        rights = muted_rights
    	
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"```Oh boy, this user is no match with my master```")
