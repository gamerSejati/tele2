import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from pyrogram.enums.parse_mode import ParseMode

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

START_TEXT = """
<i>π Hallo,</i>{}\n
<i>Saya adalah Bot Telegram yg bisa membuat link download</i>\n
<i>Klik Tombol Help untuk cara penggunaan</i>\n
<i><u>πͺππ₯π‘ππ‘π πΈ</u></i>
<b>π kontent porn, User akan dibanned.</b>\n\n
<i><b>Terima kasih</i>"""

HELP_TEXT = """
<i>- kirim file atau media dari telegram ke sini.</i>
<i>- Aku akan membuatnya jadi link yg bisa di download!.</i>
<i>- Jangan lupa bergabung di grub.</i>
<i>- Link permanent dengan speed Cepat</i>\n
<u>πΈ πͺππ₯π‘ππ‘π πΈ</u>\n
<b>π kontent porn, User akan dibanned.</b>\n
<i>Hubungi developer jika ada eror.</i> <b>: <a href='https://t.me/+iOmLoJkMhjk0Y2Rl'>[ Join Grub ]</a></b>"""

ABOUT_TEXT = """
<b>β Nama : filestreamx</b>\n
<b>πΈVersi : <a href='https://t.me/+iOmLoJkMhjk0Y2Rl'>3.0.1</a></b>\n
<b>πΉSα΄α΄Κα΄α΄ : <a href='https://t.me/+iOmLoJkMhjk0Y2Rl'>Join Grub dulu</a></b>\n
<b>πΈUpdate Versi : <a href='https://t.me/+iOmLoJkMhjk0Y2Rl'>[ 26 - α΄α΄Ι΄α΄ - 2022 ] 03:35 α΄α΄</a></b>"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hα΄Κα΄', callback_data='help'),
        InlineKeyboardButton('AΚα΄α΄α΄', callback_data='about'),
        InlineKeyboardButton('CΚα΄sα΄', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hα΄α΄α΄', callback_data='home'),
        InlineKeyboardButton('AΚα΄α΄α΄', callback_data='about'),
        InlineKeyboardButton('CΚα΄sα΄', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hα΄α΄α΄', callback_data='home'),
        InlineKeyboardButton('Hα΄Κα΄', callback_data='help'),
        InlineKeyboardButton('CΚα΄sα΄', callback_data='close')
        ]]
    )

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()

def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None


@StreamBot.on_message(filters.command('start') & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Pengguna Baru:** \n\n [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Memulai Bot !!"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Maaf , kamu sudah di Ban. Hubungi pemilik/author!\n\n Terima kasih",
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Jα΄ΙͺΙ΄ Channelku dulu π</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Jα΄ΙͺΙ΄ π", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode=ParseMode.HTML
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Ada masalah</i> <b><a href='http://t.me/budy_RangerDark'>[ α΄ΚΙͺα΄α΄ Κα΄Κα΄ ]</a></b>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text=START_TEXT.format(m.from_user.mention),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
              )                                                                         
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="**Maaf , Kamu di BAN!** @budy_RangerDark",
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**PΚα΄α΄sα΄ Jα΄ΙͺΙ΄ MΚ Uα΄α΄α΄α΄α΄s CΚα΄Ι΄Ι΄α΄Κ α΄α΄ α΄sα΄ α΄ΚΙͺs Bα΄α΄**!\n\n**Dα΄α΄ α΄α΄ Oα΄ α΄ΚΚα΄α΄α΄, OΙ΄ΚΚ CΚα΄Ι΄Ι΄α΄Κ Sα΄Κsα΄ΚΙͺΚα΄Κs α΄α΄Ι΄ α΄sα΄ α΄Κα΄ Bα΄α΄**!",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                          InlineKeyboardButton("π€ Jα΄ΙͺΙ΄ Uα΄α΄α΄α΄α΄s CΚα΄Ι΄Ι΄α΄Κ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")],
                         [InlineKeyboardButton("π Refresh / Try Again", url=f"https://t.me/{(await b.get_me()).username}?start=AvishkarPatil_{usr_cmd}")
                        
                        ]]
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Ada yg Bermasalah** [Budy Gamer](https://t.me/budy_RangerDark).",
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))
        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.id,
                                     file_name)

        msg_text ="""
<i><u>Link ini akan Expired dalam 24jam !</u></i>\n
<b>π Nama :</b> <i>{}</i>
<b>π¦ Ukuran :</b> <i>{}</i>
<b>π₯ Dα΄α΄‘Ι΄Κα΄α΄α΄ :</b> <i>{}</i>\n\n
<b>πΈ Klik Tombol Download dibawah!</b>
<i>π Terima Kasih</i> <b>@budy_RangerDark</b>
"""

        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Dα΄α΄‘Ι΄Κα΄α΄α΄ π₯", url=stream_link)]])
        )



@StreamBot.on_message(filters.private & filters.command(["about"]))
async def start(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )


@StreamBot.on_message(filters.command('help') & filters.private)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**Pengguna Baru **\n\n [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Memulai Bot !!__"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Maaf, kamu di Ban , HUbungi pemilik bot</i>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**PΚα΄α΄sα΄ Jα΄ΙͺΙ΄ MΚ Uα΄α΄α΄α΄α΄s CΚα΄Ι΄Ι΄α΄Κ α΄α΄ α΄sα΄ α΄ΚΙͺs Bα΄α΄!**\n\n__Dα΄α΄ α΄α΄ Oα΄ α΄ΚΚα΄α΄α΄, OΙ΄ΚΚ CΚα΄Ι΄Ι΄α΄Κ Sα΄Κsα΄ΚΙͺΚα΄Κs α΄α΄Ι΄ α΄sα΄ α΄Κα΄ Bα΄α΄!__",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("π€ Jα΄ΙͺΙ΄ Uα΄α΄α΄α΄α΄s CΚα΄Ι΄Ι΄α΄Κ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]]
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Ada yg bermasalah , hubungi owner [BUdy Gamer](https://t.me/budy_RangerDark).",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text=HELP_TEXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
        )

